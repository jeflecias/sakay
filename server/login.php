<?php
// connect to db 
require 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $password = $_POST["password"];

    // check if empty
    if (empty($username) || empty($password)) {
        echo "Please fill in all fields.";
        exit;
    }

    // sql statement, scan database for user
    // look for username column
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);

    // boolean true if user is found, false if not found (invalid)
    $user = $stmt->fetch();

    // verify both
    if ($user && password_verify($password, $user["password_hash"])) {
            echo json_encode([
        "status" => "success",
        "message" => "Login successful!",
        "is_passenger" => (bool) $user["is_passenger"],
        "is_driver" => (bool) $user["is_driver"]
    ]);
    }

    else {
    echo json_encode(["status" => "error", "message" => "Invalid username or password."]);
    }
}
?>
