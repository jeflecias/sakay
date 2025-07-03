<?php
require "db.php";

// Check for both user_id and rid parameters
if (!isset($_GET['user_id']) || !isset($_GET['rid'])) {
    echo json_encode(['success' => false, 'message' => 'user_id and rid required']);
    exit;
}

$user_id = intval($_GET['user_id']);
$ride_id = intval($_GET['rid']);

// Check user's ride request with proper security - match both user_id and ride_id
$stmt = $pdo->prepare("
    SELECT 
        m.pickup_lat,
        m.pickup_lng,
        m.destination_lat,
        m.destination_lng,
        ds.current_lat as driver_current_lat,
        ds.current_lng as driver_current_lng
    FROM ride_requests r
    JOIN matches m ON r.id = m.ride_request_id
    LEFT JOIN driver_status ds ON m.driver_id = ds.driver_id
    WHERE r.user_id = ? AND r.id = ? AND m.driver_progress = 'en_route' AND m.status = 'ongoing'
");

$stmt->execute([$user_id, $ride_id]);
$match = $stmt->fetch(PDO::FETCH_ASSOC);

if ($match) {
    echo json_encode([
        'success' => true,
        'pickup_coords' => ['lat' => $match['pickup_lat'], 'lng' => $match['pickup_lng']],
        'destination_coords' => ['lat' => $match['destination_lat'], 'lng' => $match['destination_lng']],
        'driver_current_coords' => ['lat' => $match['driver_current_lat'], 'lng' => $match['driver_current_lng']]
    ]);
} else {
    echo json_encode(['success' => false, 'message' => 'No en_route driver found for this ride']);
}
?>