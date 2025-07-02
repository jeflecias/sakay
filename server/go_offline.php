<?php
// opposite of go online lol

require 'db.php';

$user_id = $_POST['user_id'];

$stmt = $pdo->prepare("UPDATE drivers SET is_available = 0 WHERE user_id = ?");
$stmt->execute([$user_id]);

echo json_encode(["status" => "offline"]);
?>
