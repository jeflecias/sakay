<?php
require 'db.php';

// uses first in first out matching
$stmt = $pdo->query("SELECT * FROM ride_requests WHERE status = 'pending' ORDER BY requested_at ASC LIMIT 1");
$ride = $stmt->fetch(PDO::FETCH_ASSOC);

// returns to mainapp as json
echo json_encode($ride);
?>
