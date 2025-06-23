-- pakisabi if may want kayo tanggalin dito or i-add for user registry

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- user id must be unique
    username VARCHAR(50) NOT NULL UNIQUE,  -- username must be unique & not empty
    email VARCHAR(100) NOT NULL UNIQUE, -- email must be unique & not empty
    password_hash VARCHAR(255) NOT NULL, -- password not empty, 255 kase ihahash
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- time stamp lang
    is_passenger BOOLEAN DEFAULT FALSE, -- tinitignan kung passenger
    is_driver BOOLEAN DEFAULT FALSE -- tinitignan kung driver
);
