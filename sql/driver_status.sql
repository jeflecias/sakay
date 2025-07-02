CREATE TABLE driver_status (
    driver_id INT PRIMARY KEY,
    current_location VARCHAR(255) NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    is_online BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES users(id)
);
