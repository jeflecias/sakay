<?php
require 'db.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

try {
    // get ride id from params
    $ride_id = $_GET['ride_id'] ?? null;
    
    if (!$ride_id) {
        echo json_encode([
            'success' => false,
            'message' => 'Missing ride_id parameter'
        ]);
        exit;
    }
    
    // check for matches where driver has arrived for the specific ride
    $stmt = $pdo->prepare("
        SELECT id, ride_request_id, driver_id, driver_progress, status 
        FROM matches 
        WHERE ride_request_id = ?
        AND status = 'ongoing'
    ");
    $stmt->execute([$ride_id]);
    $matches = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // check if any other driver
    $hasArrivedDriver = false;
    $driverDetails = [];
    
    foreach ($matches as $match) {
        $driverDetails[] = [
            'driver_id' => $match['driver_id'],
            'progress' => $match['driver_progress'],
            'status' => $match['status']
        ];
        
        if ($match['driver_progress'] === 'arrived') {
            $hasArrivedDriver = true;
            break;
        }
    }
    
    // some debugs again something is going wrong again
    echo json_encode([
        'success' => true,
        'driver_arrived' => $hasArrivedDriver,
        'message' => $hasArrivedDriver ? 'Driver has arrived' : 'Driver not yet arrived',
        'ride_id' => $ride_id,
        'total_matches' => count($matches),
        'driver_details' => $driverDetails, 
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Error checking driver arrivals: ' . $e->getMessage()
    ]);
}
?>