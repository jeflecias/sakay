<?php
// just a simple script make 'not' to 'on_going' when accept is pressed
require 'db.php';

$match_id = $_POST['match_id'];
$driver_id = $_POST['driver_id'];

$sql = "UPDATE matches SET driver_progress = 'en_route' WHERE id = ? AND driver_id = ?";
$stmt = $pdo->prepare($sql);

if ($stmt->execute([$match_id, $driver_id])) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'error' => 'Update failed']);
}
?>