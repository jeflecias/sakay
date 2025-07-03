CREATE TABLE matches (
    id INT AUTO_INCREMENT PRIMARY KEY,

    ride_request_id INT NOT NULL,
    driver_id INT NOT NULL,

    match_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- passenger detail
    pickup_lat DOUBLE NOT NULL,
    pickup_lng DOUBLE NOT NULL,
    destination_lat DOUBLE NOT NULL,
    destination_lng DOUBLE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,

    -- driver's loc current
    driver_start_lat DOUBLE NOT NULL,
    driver_start_lng DOUBLE NOT NULL,

    -- Rdriver progress otw or not
    driver_progress ENUM('not', 'en_route', 'arrived', 'passenger_onboard') DEFAULT 'not',
    status ENUM('ongoing', 'completed', 'cancelled') DEFAULT 'ongoing',

    FOREIGN KEY (ride_request_id) REFERENCES ride_requests(id),
    FOREIGN KEY (driver_id) REFERENCES users(id)
);