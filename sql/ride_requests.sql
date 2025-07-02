-- store data about ride booking

-- not null = required
-- default null = may not be required

CREATE TABLE ride_requests (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    passenger_id INT NOT NULL, -- pointing to the user who request the ride
    driver_id INT DEFAULT NULL, -- points to the user who the ride is assigned to
    pickup_location VARCHAR(255) NOT NULL, -- where ride starts
    destination VARCHAR(255) NOT NULL, -- ride stop
    vehicle_type VARCHAR(50) NOT NULL, -- vehicle type
    status ENUM('pending', 'matched', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending', -- status if you are matched etc, default is pending
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- simple date
    FOREIGN KEY (passenger_id) REFERENCES users(id), 
    FOREIGN KEY (driver_id) REFERENCES users(id) -- both of these must exist in the users table if not, block
);
