<?php
require 'db.php';

// simple extraction no input validation yet
$ride_id = $_POST['ride_id'];
$driver_id = $_POST['driver_id'];

// assign driver to ride
$stmt = $pdo->prepare("UPDATE ride_requests SET driver_id = ?, status = 'matched' WHERE id = ?");
$stmt->execute([$driver_id, $ride_id]);

echo json_encode(["success" => true]);
?>
