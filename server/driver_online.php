<?php
require "db.php";

// verify first
if (!isset($_POST['current_lat'], $_POST['current_lng'], $_POST['driver_id'], $_POST['vehicle'])) {
    http_response_code(400);
    echo json_encode(["error" => "Missing required POST parameters."]);
    exit;
}

$current_lat = $_POST['current_lat'];
$current_lng = $_POST['current_lng'];
$driver_id = $_POST['driver_id'];
$vehicle = $_POST['vehicle'];

try {
    // check if online
    $stmt = $pdo->prepare("SELECT id FROM driver_status WHERE driver_id = ?");
    $stmt->execute([$driver_id]);

    if ($stmt->fetch()) {
        $update = $pdo->prepare("
            UPDATE driver_status 
            SET current_lat = ?, current_lng = ?, vehicle_type = ?, status = 'online', updated_at = NOW()
            WHERE driver_id = ?
        ");
        $update->execute([$current_lat, $current_lng, $vehicle, $driver_id]);
    } else {
        $insert = $pdo->prepare("
            INSERT INTO driver_status (driver_id, current_lat, current_lng, vehicle_type, status)
            VALUES (?, ?, ?, ?, 'online')
        ");
        $insert->execute([$driver_id, $current_lat, $current_lng, $vehicle]);
    }

    echo json_encode(["success" => true]);

// added this because something is going wrong
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["error" => "Database error", "details" => $e->getMessage()]);
}
