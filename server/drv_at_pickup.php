<?php
require 'db.php';

$driver_id = $_POST['driver_id'];
$ride_request_id = $_POST['ride_request_id'];

// Update driver to arrived
$query = "UPDATE matches 
          SET driver_progress = 'arrived' 
          WHERE driver_id = ? AND ride_request_id = ?";

$stmt = $pdo->prepare($query);

if ($stmt->execute([$driver_id, $ride_request_id])) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'error' => 'Update failed']);
}
?>