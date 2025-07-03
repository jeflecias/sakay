<?php
require "db.php";

// added thes bececause there was some error i dont understnad
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

$method = $_SERVER['REQUEST_METHOD'];
$driver_id = $_GET['driver_id'] ?? $_POST['driver_id'] ?? null;

if (!$driver_id) {
    echo json_encode(['error' => 'Driver ID is required']);
    exit;
}

try {
    if ($method === 'POST') {
        // handle accept and reject stiff
        $match_id = $_POST['match_id'] ?? null;
        $action = $_POST['action'] ?? null;
        
        if (!$match_id || !$action) {
            echo json_encode(['error' => 'Match ID and action are required']);
            exit;
        }
        
        $pdo->beginTransaction();
        
        if ($action === 'accept') {
            // match to accepted
            $stmt = $pdo->prepare("
                UPDATE matches 
                SET driver_accepted = TRUE, driver_response_time = NOW() 
                WHERE id = ? AND driver_id = ? AND driver_accepted = FALSE
            ");
            $stmt->execute([$match_id, $driver_id]);
            
            // status to match
            $pdo->prepare("
                UPDATE ride_requests r
                JOIN matches m ON r.id = m.ride_request_id
                SET r.status = 'matched'
                WHERE m.id = ?
            ")->execute([$match_id]);
            
            $pdo->prepare("
                UPDATE driver_status 
                SET status = 'matched' 
                WHERE driver_id = ?
            ")->execute([$driver_id]);
            
            $pdo->commit();
            echo json_encode(['success' => true, 'message' => 'Match accepted']);
            
        } elseif ($action === 'reject') {
            // cancel the match
            $stmt = $pdo->prepare("
                UPDATE matches 
                SET status = 'cancelled', driver_response_time = NOW() 
                WHERE id = ? AND driver_id = ? AND driver_accepted = FALSE
            ");
            $stmt->execute([$match_id, $driver_id]);
            
            // free passenger and driver
            $pdo->prepare("
                UPDATE ride_requests r
                JOIN matches m ON r.id = m.ride_request_id
                SET r.status = 'pending'
                WHERE m.id = ?
            ")->execute([$match_id]);
            
            $pdo->prepare("
                UPDATE driver_status 
                SET status = 'online' 
                WHERE driver_id = ?
            ")->execute([$driver_id]);

            $pdo->prepare("
                UPDATE matches 
                SET status = 'matched'
                WHERE id = ?
            ")->execute([$match_id]);
            
            $pdo->commit();
            echo json_encode(['success' => true, 'message' => 'Match rejected']);
        }
        
    } else {
        // getreq return pending match
        $stmt = $pdo->prepare("
            SELECT m.*, r.user_id as passenger_id, r.created_at as request_time
            FROM matches m
            JOIN ride_requests r ON m.ride_request_id = r.id
            WHERE m.driver_id = ? 
            AND m.driver_accepted = 0
            AND m.status = 'ongoing'
            ORDER BY m.match_time DESC
        ");
        $stmt->execute([$driver_id]);
        $pending_matches = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        // get accepted match
        $stmt = $pdo->prepare("
            SELECT m.*, r.user_id as passenger_id, r.created_at as request_time
            FROM matches m
            JOIN ride_requests r ON m.ride_request_id = r.id
            WHERE m.driver_id = ? 
            AND m.driver_accepted = 1
            AND m.status = 'ongoing'
            ORDER BY m.match_time DESC
        ");
        $stmt->execute([$driver_id]);
        $accepted_matches = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        echo json_encode([
            'pending_matches' => $pending_matches,
            'accepted_matches' => $accepted_matches
        ]);
    }
    
} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    echo json_encode(['error' => $e->getMessage()]);
}
?>