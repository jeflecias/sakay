<?php
require 'db.php';

$ride_id = $_POST['ride_id'];
$driver_id = $_POST['driver_id'];

$stmt = $pdo->prepare("UPDATE ride_requests SET driver_id = ?, status = 'matched' WHERE id = ?");
$stmt->execute([$driver_id, $ride_id]);

echo json_encode(["success" => true]);
?>
