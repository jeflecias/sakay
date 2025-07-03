<?php

// same login php as before
require 'db.php';
header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // input validation 
    $username = htmlspecialchars(trim($_POST["username"]));
    $password = $_POST["password"];

    if (empty($username) || empty($password)) {
        echo json_encode([
            "status" => "error",
            "message" => "Please fill in all fields."
        ]);
        exit;
    }

    // find in the table
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    // verify then hash
    if ($user && password_verify($password, $user["password_hash"])) {
        echo json_encode([
            "status" => "success",
            "user_id" => $user["id"],
            "message" => "Login successful!",
            "is_passenger" => (bool) $user["is_passenger"],
            "is_driver" => (bool) $user["is_driver"]
        ]);
    } else {
        echo json_encode([
            "status" => "error",
            "message" => "Invalid username or password."
        ]);
    }
}
?>
