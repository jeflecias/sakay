<?php
require 'db.php';

// had to put this because it was raising some errors again
// i dont want to toouch this anymore i might breka it again
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

try {
    // extract
    $user_id = $_POST['user_id'] ?? null;
    $ride_id = $_POST['ride_id'] ?? null;
    
    if (!$user_id || !$ride_id) {
        echo json_encode([
            'success' => false,
            'message' => 'Missing user_id or ride_id'
        ]);
        exit;
    }
    
    // update passenger arrival to onboard
    $stmt = $pdo->prepare("
        UPDATE matches 
        SET driver_progress = 'passenger_onboard' 
        WHERE ride_request_id = ? 
        AND driver_progress = 'arrived'
        AND status = 'ongoing'
    ");
    
    $result = $stmt->execute([$ride_id]);
    
    if ($result && $stmt->rowCount() > 0) {
        echo json_encode([
            'success' => true,
            'message' => 'Passenger is now onboard',
            'updated_rows' => $stmt->rowCount()
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'No matching ride found or driver not yet arrived'
        ]);
    }
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Error updating passenger status: ' . $e->getMessage()
    ]);
}
?>