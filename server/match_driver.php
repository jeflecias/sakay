<?php
require 'db.php';

// this is for the matchmaking

// get one pending ride
$ride_stmt = $pdo->query("SELECT * FROM ride_requests WHERE status = 'pending' LIMIT 1");
$ride = $ride_stmt->fetch();

if ($ride) {
    $vehicle_type = $ride['vehicle_type'];

    // finid available driver, must match the vehicle that the user entered as well
    $driver_stmt = $pdo->prepare("SELECT * FROM drivers WHERE is_available = 1 AND vehicle_type = ? LIMIT 1");
    $driver_stmt->execute([$vehicle_type]);
    $driver = $driver_stmt->fetch();

    if ($driver) {
        // now assign driver to that ride
        $match_stmt = $pdo->prepare("UPDATE ride_requests SET matched_driver_id = ?, status = 'matched' WHERE id = ?");
        $match_stmt->execute([$driver['user_id'], $ride['id']]);

        // set driver to unavailable
        $update_driver = $pdo->prepare("UPDATE drivers SET is_available = 0 WHERE user_id = ?");
        $update_driver->execute([$driver['user_id']]);

        echo json_encode(["status" => "matched", "ride_id" => $ride['id'], "driver_id" => $driver['user_id']]);
    } else {
        echo json_encode(["status" => "no_driver_available"]);
    }
} else {
    echo json_encode(["status" => "no_pending_ride"]);
}
?>
