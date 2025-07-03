<?php
include 'db.php';
try {
    $ride_id = isset($_POST['ride_id']) ? intval($_POST['ride_id']) : 0;
    $user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
    
    if (!$ride_id || !$user_id) {
        echo json_encode([
            'success' => false,
            'message' => 'Missing required parameters: ride_id and user_id'
        ]);
        exit;
    }
    
    $pdo->beginTransaction();
    
    // verify if belongs to user
    $verify_stmt = $pdo->prepare("
        SELECT 
            m.id as match_id,
            m.status,
            m.driver_progress,
            m.driver_id,
            rr.user_id as passenger_id
        FROM matches m
        INNER JOIN ride_requests rr ON m.ride_request_id = rr.id
        WHERE m.ride_request_id = :ride_id 
        AND rr.user_id = :user_id
        AND m.status = 'ongoing'
        ORDER BY m.match_time DESC
        LIMIT 1
    ");
    
    $verify_stmt->bindParam(':ride_id', $ride_id, PDO::PARAM_INT);
    $verify_stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $verify_stmt->execute();
    
    $match = $verify_stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$match) {
        $pdo->rollBack();
        echo json_encode([
            'success' => false,
            'message' => 'No active ride found for the given ride_id and user_id'
        ]);
        exit;
    }
    
    // check if passngr is on board 
    if ($match['driver_progress'] !== 'passenger_onboard') {
        $pdo->rollBack();
        echo json_encode([
            'success' => false,
            'message' => 'Trip cannot be finished. Passenger must be onboard first.',
            'current_progress' => $match['driver_progress']
        ]);
        exit;
    }
    
    // update match status to complete because finished
    $update_stmt = $pdo->prepare("
        UPDATE matches 
        SET status = 'completed'
        WHERE id = :match_id
    ");
    
    $update_stmt->bindParam(':match_id', $match['match_id'], PDO::PARAM_INT);
    $update_stmt->execute();
    
    // update
    $update_request_stmt = $pdo->prepare("
        UPDATE ride_requests 
        SET status = 'completed'
        WHERE id = :ride_id
    ");
    
    $update_request_stmt->bindParam(':ride_id', $ride_id, PDO::PARAM_INT);
    $update_request_stmt->execute();
    
    $pdo->commit();
    

    // check for errors 
    error_log("Trip finished by passenger - Ride ID: $ride_id, User ID: $user_id, Match ID: {$match['match_id']}");
    echo json_encode([
        'success' => true,
        'message' => 'Trip completed successfully',
        'ride_id' => $ride_id,
        'match_id' => $match['match_id'],
        'driver_id' => $match['driver_id'],
        'completion_time' => date('Y-m-d H:i:s'),
        'completed_by' => 'passenger'
    ]);
    
} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    
    error_log("Error in finish_trip.php: " . $e->getMessage());
    echo json_encode([
        'success' => false,
        'message' => 'An error occurred while finishing the trip',
        'error' => $e->getMessage()
    ]);
}
?>