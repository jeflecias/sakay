<?php
// connect to db
require 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    file_put_contents(__DIR__ . "/debug_post.txt", print_r($_POST, true));
    $username = trim($_POST["username"]);
    $email = trim($_POST["email"]);
    $password = $_POST["password"];
    $is_passenger = (int) $_POST["is_passenger"];
    $is_driver = (int) $_POST["is_driver"];

    // check if empty
    if (empty($username) || empty($email) || empty($password)) {
        echo "Please fill in all fields.";
        exit;
    }

    // hash para secure
    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    // sql statement, basically in-insert nya into the users table
    $stmt = $pdo->prepare("INSERT INTO users (username, email, password_hash, is_passenger, is_driver) VALUES (?, ?, ?, ?, ?)");

    try {
        $stmt->execute([$username, $email, $password_hash, $is_passenger, $is_driver]);
        echo "Registration successful!";
    } catch (PDOException $e) {
        // pag 23000, duplicate, tapos mag error
        if ($e->getCode() == 23000) {
            echo "Username or email already exists.";
        } else {
            echo "Registration failed: " . $e->getMessage();
        }
    }
}
?>
