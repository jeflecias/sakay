<?php

// this just connects to the ping func in tkinter to check if its driver is still there then send the reqs to matchqueue then
// if not here remove that driver
require "db.php";

if (!isset($_POST['driver_id'])) {
    echo json_encode(["success" => false, "message" => "Missing driver_id"]);
    exit;
}

$driver_id = $_POST['driver_id'];

$stmt = $pdo->prepare("UPDATE driver_status SET updated_at = NOW() WHERE driver_id = ? AND status = 'online'");
$stmt->execute([$driver_id]);

echo json_encode(["success" => true]);
?>