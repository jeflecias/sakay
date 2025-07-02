<?php
// connect to db as usual
require 'db.php';

// extract these
$user_id = $_POST['user_id'];
$location = $_POST['location'];
$vehicle = $_POST['vehicle_type'];

$stmt = $pdo->prepare("REPLACE INTO drivers (user_id, location, vehicle_type, is_available) VALUES (?, ?, ?, 1)");
$stmt->execute([$user_id, $location, $vehicle]);

echo json_encode(["status" => "online"]);
?>
