<?php
// credentials, naka localhost muna, tetesting ko pa
$host = "localhost";
$dbname = "tkapp_db";
$username = "sakay";
$password = "ready";

// check for errors
try {
    // connect to db
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // pdo error mode attribute, throw exception when db error
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}
?>
