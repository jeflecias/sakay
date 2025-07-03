<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

require 'db.php';

// Get POST data
$input = json_decode(file_get_contents('php://input'), true);
$ride_request_id = isset($input['ride_request_id']) ? $input['ride_request_id'] : null;
$driver_id = isset($input['driver_id']) ? $input['driver_id'] : null;

// Validate input
if (!$ride_request_id || !$driver_id) {
    echo json_encode(['success' => false, 'error' => 'Missing ride_request_id or driver_id']);
    exit;
}

try {
    // Check if there's a match with driver_progress = 'passenger_onboard'
    $stmt = $pdo->prepare("
        SELECT 
            id,
            ride_request_id,
            driver_id,
            pickup_lat,
            pickup_lng,
            destination_lat,
            destination_lng,
            vehicle_type,
            driver_start_lat,
            driver_start_lng,
            driver_progress,
            status
        FROM matches 
        WHERE ride_request_id = :ride_request_id 
        AND driver_id = :driver_id 
        AND driver_progress = 'passenger_onboard'
        AND status = 'ongoing'
    ");
    
    $stmt->bindParam(':ride_request_id', $ride_request_id, PDO::PARAM_INT);
    $stmt->bindParam(':driver_id', $driver_id, PDO::PARAM_INT);
    $stmt->execute();
    
    $match = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($match) {
        // Match found with passenger_onboard status
        echo json_encode([
            'success' => true,
            'passenger_onboard' => true,
            'data' => [
                'match_id' => $match['id'],
                'ride_request_id' => $match['ride_request_id'],
                'driver_id' => $match['driver_id'],
                'pickup_lat' => $match['pickup_lat'],
                'pickup_lng' => $match['pickup_lng'],
                'destination_lat' => $match['destination_lat'],
                'destination_lng' => $match['destination_lng'],
                'vehicle_type' => $match['vehicle_type'],
                'driver_start_lat' => $match['driver_start_lat'],
                'driver_start_lng' => $match['driver_start_lng'],
                'driver_progress' => $match['driver_progress'],
                'status' => $match['status']
            ]
        ]);
    } else {
        // No match found or not in passenger_onboard status
        echo json_encode([
            'success' => true,
            'passenger_onboard' => false,
            'message' => 'No match found with passenger_onboard status'
        ]);
    }
    
} catch(PDOException $e) {
    echo json_encode(['success' => false, 'error' => 'Database error: ' . $e->getMessage()]);
}
?>