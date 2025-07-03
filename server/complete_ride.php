<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require 'db.php';

$driver_id = $_POST['driver_id'];
$ride_request_id = $_POST['ride_request_id'];

// Update status to 'completed'
$query = "UPDATE matches 
          SET status = 'completed' 
          WHERE driver_id = ? AND ride_request_id = ?";
$stmt = $pdo->prepare($query);

if ($stmt->execute([$driver_id, $ride_request_id])) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'error' => 'Update failed']);
}
?>