<?php
require 'db.php';

$ride_id = $_POST['ride_id'];

// set to cancelled, can work for either passenger or driver
$stmt = $pdo->prepare("UPDATE ride_requests SET status = 'cancelled' WHERE id = ?");
$stmt->execute([$ride_id]);

// setting to status is better i think
echo json_encode(["status" => "cancelled"]);
?>
