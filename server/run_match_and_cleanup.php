<?php
require "db.php";

// clean users who havent pinged forawhile
$pdo->exec("DELETE FROM driver_status WHERE updated_at < NOW() - INTERVAL 30 SECOND AND status = 'online'");
$pdo->exec("DELETE FROM ride_requests WHERE created_at < NOW() - INTERVAL 30 SECOND AND status = 'pending'");

// fetch pending ride requests, first in first out similar to those inventory stuff puregold haahhahahaha
$passengers = $pdo->query("SELECT * FROM ride_requests WHERE status = 'pending' ORDER BY created_at")->fetchAll();

foreach ($passengers as $passenger) {
    $vehicle = $passenger['vehicle_type'];
    echo "Looking for {$vehicle} driver for passenger {$passenger['user_id']}\n";

    // find matching driver
    $stmt = $pdo->prepare("SELECT * FROM driver_status WHERE status = 'online' AND vehicle_type = ? ORDER BY updated_at DESC LIMIT 1");
    $stmt->execute([$vehicle]);
    $driver = $stmt->fetch();

    // if not, skip
    if (!$driver) {
        echo "No available {$vehicle} driver found\n";
        continue;
    }

    echo "Found driver {$driver['driver_id']}\n";

    try {
        // begin transaction now
        $pdo->beginTransaction();

        // update ride req status (removed driver_id reference that was causing the error)
        $update_ride = $pdo->prepare("UPDATE ride_requests SET status = 'matched' WHERE id = ? AND status = 'pending'");
        $update_ride->execute([$passenger['id']]);

        // update driver status to matched
        $update_driver = $pdo->prepare("UPDATE driver_status SET status = 'matched' WHERE driver_id = ? AND status = 'online'");
        $update_driver->execute([$driver['driver_id']]);

        // insert matched users in matches table
        $insert_match = $pdo->prepare("
            INSERT INTO matches (
                ride_request_id, driver_id, match_time,
                pickup_lat, pickup_lng, destination_lat, destination_lng,
                vehicle_type, driver_start_lat, driver_start_lng
            ) VALUES (?, ?, NOW(), ?, ?, ?, ?, ?, ?, ?)
        ");

        $insert_match->execute([
            $passenger['id'],
            $driver['driver_id'],
            $passenger['pickup_lat'],
            $passenger['pickup_lng'],
            $passenger['destination_lat'],
            $passenger['destination_lng'],
            $vehicle,
            $driver['current_lat'],
            $driver['current_lng']
        ]);

        // do the transac
        $pdo->commit();
        echo "✓ Matched passenger {$passenger['user_id']} with driver {$driver['driver_id']}\n";
    } catch (Exception $e) {
        $pdo->rollBack();
        echo "✗ Error matching passenger {$passenger['user_id']}: " . $e->getMessage() . "\n";
        error_log("Database error in matching script: " . $e->getMessage());
    }
}

echo "Match & cleanup cycle completed at " . date("Y-m-d H:i:s") . "\n";
?>