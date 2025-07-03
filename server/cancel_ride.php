<?php
// simple cancel ride
require "db.php";

if (!isset($_POST['uid'])) {
    echo json_encode(["success" => false, "message" => "Missing user ID"]);
    exit;
}

$uid = $_POST['uid'];

// cancel if ride only if on wait
$stmt = $pdo->prepare("UPDATE ride_requests SET status = 'cancelled' WHERE user_id = ? AND status = 'waiting'");
$stmt->execute([$uid]);

if ($stmt->rowCount() > 0) {
    echo json_encode(["success" => true, "message" => "Ride cancelled"]);
} else {
    echo json_encode(["success" => false, "message" => "No active ride to cancel or already matched"]);
}
?>
