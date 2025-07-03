<?php
require "db.php";

// this just connects to the ping func in tkinter to check if its driver is still there then send the reqs to matchqueue then
// if not here remove that passenger

if (!isset($_POST['user_id'])) {
    echo json_encode(["success" => false, "message" => "Missing user_id"]);
    exit;
}

$stmt = $pdo->prepare("
    UPDATE ride_requests 
    SET created_at = NOW() 
    WHERE user_id = ? AND status = 'pending'
");
$stmt->execute([$_POST['user_id']]);

echo json_encode(["success" => true]);
?>
