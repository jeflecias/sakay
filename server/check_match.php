<?php
require 'db.php';

// simple extraction no input validation yet
$passenger_id = $_GET['passenger_id'];

// retrieves most recent ride req for passenger
$stmt = $pdo->prepare("SELECT * FROM ride_requests WHERE passenger_id = ? ORDER BY requested_at DESC LIMIT 1");
$stmt->execute([$passenger_id]);
$ride = $stmt->fetch(PDO::FETCH_ASSOC);

// returns to mainapp as json
echo json_encode($ride);
?>
