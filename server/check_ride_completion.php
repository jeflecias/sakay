<?php
require 'db.php';


// placed this again because of errors
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

// input validation
if (!isset($_GET['ride_id']) || empty($_GET['ride_id'])) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => 'Ride ID is required'
    ]);
    exit();
}

$ride_id = $_GET['ride_id'];
$user_id = isset($_GET['user_id']) ? $_GET['user_id'] : null;

try {
    // check if ride status is complete
    $stmt = $pdo->prepare("
        SELECT 
            id,
            ride_request_id,
            driver_id,
            status,
            driver_progress,
            driver_accepted,
            match_time
        FROM matches 
        WHERE ride_request_id = :ride_id
        ORDER BY match_time DESC
        LIMIT 1
    ");
    
    $stmt->bindParam(':ride_id', $ride_id, PDO::PARAM_INT);
    $stmt->execute();
    
    $match = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($match) {
        // check if status is completed
        $ride_completed = ($match['status'] === 'completed');
        
        // additional check might get an error 
        $driver_finished = ($match['driver_progress'] === 'passenger_onboard' || 
                           $match['driver_progress'] === 'arrived');
        
        echo json_encode([
            'success' => true,
            'ride_completed' => $ride_completed,
            'can_finish_trip' => $ride_completed,
            'match_details' => [
                'match_id' => $match['id'],
                'ride_request_id' => $match['ride_request_id'],
                'driver_id' => $match['driver_id'],
                'status' => $match['status'],
                'driver_progress' => $match['driver_progress'],
                'driver_accepted' => (bool)$match['driver_accepted'],
                'match_time' => $match['match_time']
            ],
            'message' => $ride_completed ? 'Ride completed - finish trip button enabled' : 
                        'Ride not yet completed - finish trip button disabled'
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'ride_completed' => false,
            'can_finish_trip' => false,
            'message' => 'No match found for this ride ID'
        ]);
    }
    
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}

$pdo = null;
?>