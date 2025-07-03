<?php
require "db.php";

// Added these because there was some error i dont understand
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
        // Handle accept and reject actions
        $match_id = $_POST['match_id'] ?? null;
        $action = $_POST['action'] ?? null;
        
        if (!$match_id || !$action) {
            echo json_encode(['error' => 'Match ID and action are required']);
            exit;
        }
        
        $pdo->beginTransaction();
        
        if ($action === 'accept') {
            // Update match to accepted
            $stmt = $pdo->prepare("
                UPDATE matches 
                SET driver_accepted = TRUE, driver_response_time = NOW() 
                WHERE id = ? AND driver_id = ? AND driver_accepted = FALSE AND status = 'ongoing'
            ");
            $result = $stmt->execute([$match_id, $driver_id]);
            
            // Check if the update actually affected any rows
            if ($stmt->rowCount() == 0) {
                $pdo->rollBack();
                echo json_encode(['error' => 'Match not found or already processed']);
                exit;
            }
            
            // Update ride request status to matched
            $pdo->prepare("
                UPDATE ride_requests r
                JOIN matches m ON r.id = m.ride_request_id
                SET r.status = 'matched'
                WHERE m.id = ?
            ")->execute([$match_id]);
            
            // Update driver status to matched
            $pdo->prepare("
                UPDATE driver_status 
                SET status = 'matched' 
                WHERE driver_id = ?
            ")->execute([$driver_id]);
            
            $pdo->commit();
            echo json_encode(['success' => true, 'message' => 'Match accepted']);
            
        } elseif ($action === 'reject') {
            // Cancel the match
            $stmt = $pdo->prepare("
                UPDATE matches 
                SET status = 'cancelled', driver_response_time = NOW() 
                WHERE id = ? AND driver_id = ? AND driver_accepted = FALSE AND status = 'ongoing'
            ");
            $result = $stmt->execute([$match_id, $driver_id]);
            
            // Check if the update actually affected any rows
            if ($stmt->rowCount() == 0) {
                $pdo->rollBack();
                echo json_encode(['error' => 'Match not found or already processed']);
                exit;
            }
            
            // Return ride request to pending status
            $pdo->prepare("
                UPDATE ride_requests r
                JOIN matches m ON r.id = m.ride_request_id
                SET r.status = 'pending'
                WHERE m.id = ?
            ")->execute([$match_id]);
            
            // Return driver to online status
            $pdo->prepare("
                UPDATE driver_status 
                SET status = 'online' 
                WHERE driver_id = ?
            ")->execute([$driver_id]);
            
            $pdo->commit();
            echo json_encode(['success' => true, 'message' => 'Match rejected']);
        } else {
            echo json_encode(['error' => 'Invalid action. Use "accept" or "reject"']);
        }
        
    } else {
        // GET request - return pending and accepted matches
        
        // Get pending matches (not yet accepted by driver)
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
        
        // Get accepted matches (accepted by driver)
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