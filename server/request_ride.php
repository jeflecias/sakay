<?php
require 'db.php';

# extract stuff
$passenger_id = $_POST['passenger_id'];
$pickup = $_POST['pickup_location'];
$destination = $_POST['destination'];
$vehicle = $_POST['vehicle_type'];

# insert into table for matching later
$stmt = $pdo->prepare("INSERT INTO ride_requests (passenger_id, pickup_location, destination, vehicle_type) VALUES (?, ?, ?, ?)");
$stmt->execute([$passenger_id, $pickup, $destination, $vehicle]);

echo json_encode(["status" => "requested"]);
?>
