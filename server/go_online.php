<?php
require 'db.php';

// from driver, tells db if go online

// check req post nnman
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    // extract as usual
    $driver_id = $_POST['driver_id'];
    $location = $_POST['location'];
    $vehicle = $_POST['vehicle'];

    // insert into table
    $stmt = $pdo->prepare("UPDATE drivers SET status = 'online', location = ?, vehicle = ? WHERE id = ?");
    $stmt->execute([$location, $vehicle, $driver_id]);

    echo json_encode(["success" => true, "message" => "Driver is now online"]);
}
?>
