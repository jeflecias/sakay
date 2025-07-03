<?php
require "db.php";

$uid = $_GET['uid'];

// check if match stuff
$stmt = $pdo->prepare("SELECT * FROM ride_requests WHERE user_id = ? AND status = 'matched' LIMIT 1");
$stmt->execute([$uid]);
$ride = $stmt->fetch();

if ($ride) {
    $driver_id = $ride['driver_id'];

    $driver_stmt = $pdo->prepare("SELECT u.username AS name, d.current_location_lat AS lat, d.current_location_lng AS lng FROM driver_status d JOIN users u ON d.driver_id = u.id WHERE d.driver_id = ?");
    $driver_stmt->execute([$driver_id]);
    $driver = $driver_stmt->fetch();

    echo json_encode(["matched" => true, "driver" => $driver]);
    exit;
}

echo json_encode(["matched" => false]);
?>