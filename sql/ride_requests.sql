-- store data about ride booking

-- not null = required
-- default null = may not be required

CREATE TABLE ride_requests (
    id INT AUTO_INCREMENT PRIMARY KEY, -- identifier
    passenger_id INT NOT NULL, -- id of passenger
    pickup_location VARCHAR(100), -- from
    destination VARCHAR(100), -- to where
    vehicle_type VARCHAR(50), -- required for matching
    status ENUM('pending', 'matched', 'cancelled', 'completed') DEFAULT 'pending', -- simple enum to show
    matched_driver_id INT DEFAULT NULL, -- its here now
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- date
    FOREIGN KEY (passenger_id) REFERENCES users(id), 
    FOREIGN KEY (matched_driver_id) REFERENCES users(id) -- reference to users
);



