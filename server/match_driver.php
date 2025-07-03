<?php
// match_driver.php
require "db.php";

// Get unassigned ride
$ride_stmt = $pdo->prepare("SELECT * FROM ride_requests WHERE status = 'waiting' LIMIT 1");
$ride_stmt->execute();
$ride = $ride_stmt->fetch();

if ($ride) {
    $vehicle = $ride['vehicle_type'];

    // Find an available driver
    $driver_stmt = $pdo->prepare("SELECT * FROM driver_status WHERE vehicle_type = ? LIMIT 1");
    $driver_stmt->execute([$vehicle]);
    $driver = $driver_stmt->fetch();

    if ($driver) {
        // Assign driver to ride
        $update_stmt = $pdo->prepare("UPDATE ride_requests SET status = 'matched', driver_id = ? WHERE id = ?");
        $update_stmt->execute([$driver['driver_id'], $ride['id']]);

        echo json_encode([
            "success" => true,
            "matched_ride" => $ride,
            "driver" => $driver
        ]);
        exit;
    }
}

echo json_encode(["success" => false, "message" => "No match found yet."]);
?>