-- store data about ride booking

-- not null = required
-- default null = may not be required

CREATE TABLE ride_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pickup_lat DOUBLE NOT NULL,
    pickup_lng DOUBLE NOT NULL,
    destination_lat DOUBLE NOT NULL,
    destination_lng DOUBLE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'matched', 'completed', 'cancelled') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);



