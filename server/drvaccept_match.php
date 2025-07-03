<?php
require "db.php";

// CORS headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['error' => 'Only POST method allowed']);
    exit;
}

$driver_id = $_POST['driver_id'] ?? null;
$match_id = $_POST['match_id'] ?? null;

if (!$driver_id || !$match_id) {
    echo json_encode(['error' => 'Driver ID and Match ID are required']);
    exit;
}

try {
    $pdo->beginTransaction();
    
    // Update driver progress from 'not' to 'en_route' in matches table only
    $stmt = $pdo->prepare("
        UPDATE matches 
        SET driver_progress = 'en_route' 
        WHERE id = ? 
        AND driver_id = ? 
        AND driver_accepted = 1 
        AND driver_progress = 'not'
        AND status = 'ongoing'
    ");
    
    $stmt->execute([$match_id, $driver_id]);
    $affected_rows = $stmt->rowCount();
    
    if ($affected_rows == 0) {
        $pdo->rollBack();
        echo json_encode([
            'error' => 'Could not update driver progress - conditions not met'
        ]);
        exit;
    }
    
    $pdo->commit();
    
    echo json_encode([
        'success' => true, 
        'message' => 'Driver is now en route to pickup location',
        'driver_progress' => 'en_route',
        'affected_rows' => $affected_rows
    ]);
    
} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    echo json_encode(['error' => $e->getMessage()]);
}
?>