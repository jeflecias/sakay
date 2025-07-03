<?php

// added this because some error again idk
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require 'db.php';

try {
    $user_id = $_POST['user_id'] ?? null;
    
    if (!$user_id) {
        echo json_encode(['error' => 'User ID required']);
        exit;
    }
    
    // get active ride match with coordinates
    $stmt = $pdo->prepare("
        SELECT 
            m.driver_progress, 
            m.status, 
            m.driver_start_lat,
            m.driver_start_lng,
            m.pickup_lat,
            m.pickup_lng,
            u.full_name as driver_name
        FROM matches m
        JOIN ride_requests rr ON m.ride_request_id = rr.id
        JOIN users u ON m.driver_id = u.id
        WHERE rr.passenger_id = ? AND m.status = 'ongoing'
        ORDER BY m.match_time DESC LIMIT 1
    ");
    
    $stmt->execute([$user_id]);
    $match = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$match) {
        echo json_encode(['status' => 'no_match']);
        exit;
    }
    
    echo json_encode([
        'status' => 'success',
        'driver_progress' => $match['driver_progress'],
        'driver_name' => $match['driver_name'],
        'driver_lat' => $match['driver_start_lat'],
        'driver_lng' => $match['driver_start_lng'],
        'pickup_lat' => $match['pickup_lat'],
        'pickup_lng' => $match['pickup_lng'],
        'is_en_route' => $match['driver_progress'] === 'en_route'
    ]);
    
} catch (Exception $e) {
    echo json_encode(['error' => 'Error: ' . $e->getMessage()]);
}
?>