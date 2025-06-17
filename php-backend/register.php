<?php
// connect to db
require 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $email = trim($_POST["email"]);
    $password = $_POST["password"];

    // check if empty
    if (empty($username) || empty($email) || empty($password)) {
        echo "Please fill in all fields.";
        exit;
    }

    // hash para secure
    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    // sql statement, basically in-insert nya into the users table
    $stmt = $pdo->prepare("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)");

    try {
        $stmt->execute([$username, $email, $password_hash]);
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
