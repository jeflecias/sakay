-- driver for matching
-- not null = required

-- on delete cascade idk if a user on a row is deleted all rows in the reference is deleted to
-- had to add bcause of some error

CREATE TABLE driver_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT NOT NULL,
    current_lat DOUBLE NOT NULL,
    current_lng DOUBLE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    status ENUM('online', 'matched', 'offline') DEFAULT 'offline',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (driver_id) REFERENCES users(id)
);
