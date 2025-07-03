<?php
require "db.php";

// validate param
if (!isset($_POST['user_id']) || !isset($_POST['pickup_lat']) || !isset($_POST['pickup_lng']) || 
    !isset($_POST['destination_lat']) || !isset($_POST['destination_lng']) || !isset($_POST['vehicle'])) {
    echo json_encode(['success' => false, 'message' => 'Missing required parameters']);
    exit;
}

$user_id = $_POST['user_id'];
$pickup_lat = $_POST['pickup_lat'];
$pickup_lng = $_POST['pickup_lng'];
$destination_lat = $_POST['destination_lat'];
$destination_lng = $_POST['destination_lng'];
$vehicle = $_POST['vehicle'];

try {
    $stmt = $pdo->prepare("
        INSERT INTO ride_requests (user_id, pickup_lat, pickup_lng, destination_lat, destination_lng, vehicle_type, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
    ");
    
    $stmt->execute([
        $user_id, $pickup_lat, $pickup_lng,
        $destination_lat, $destination_lng, $vehicle
    ]);

    $ride_request_id = $pdo->lastInsertId();

    echo json_encode([
        "success" => true,
        "ride_request_id" => $ride_request_id,
        "message" => "Ride request created successfully"
    ]);

} catch (Exception $e) {
    echo json_encode([
        "success" => false,
        "message" => "Database error: " . $e->getMessage()
    ]);
}
?>