<?php
require 'db.php';

//  from rider, sends ride req to database

// check if req method post
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // extract stuff
    $passenger_id = $_POST['passenger_id'];
    $pickup = $_POST['pickup'];
    $destination = $_POST['destination'];

    // insert into table
    $stmt = $pdo->prepare("INSERT INTO ride_requests (passenger_id, pickup, destination, status) VALUES (?, ?, ?, 'waiting')");
    $stmt->execute([$passenger_id, $pickup, $destination]);

    echo json_encode(["success" => true, "message" => "Ride requested"]);
}
?>
