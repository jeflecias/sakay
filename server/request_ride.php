<?php
require "db.php";

$user_id = $_POST['user_id'];
$pickup_lat = $_POST['pickup_lat'];
$pickup_lng = $_POST['pickup_lng'];
$destination_lat = $_POST['destination_lat'];
$destination_lng = $_POST['destination_lng'];
$vehicle = $_POST['vehicle'];

$stmt = $pdo->prepare("
    INSERT INTO ride_requests (user_id, pickup_lat, pickup_lng, destination_lat, destination_lng, vehicle_type, status)
    VALUES (?, ?, ?, ?, ?, ?, 'pending')
");
$stmt->execute([
    $user_id, $pickup_lat, $pickup_lng,
    $destination_lat, $destination_lng, $vehicle
]);

echo json_encode(["success" => true]);
