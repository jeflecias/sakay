-- holds realtime info about the driver
-- not null = required

CREATE TABLE driver_status (
    driver_id INT PRIMARY KEY, -- simple identifier
    current_location VARCHAR(255) NOT NULL, -- driver's location
    vehicle_type VARCHAR(50) NOT NULL, -- driver's vehicle type, must match with the ride req
    is_online BOOLEAN DEFAULT FALSE, -- is online, default is not (meaning drivr is offline on default)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- simple date
    FOREIGN KEY (driver_id) REFERENCES users(id) -- must exist on users, if not, block
);
