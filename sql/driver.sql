-- driver for matching
-- not null = required

-- on delete cascade idk if a user on a row is deleted all rows in the reference is deleted to
-- had to add bcause of some error

CREATE TABLE drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location VARCHAR(100),
    vehicle_type VARCHAR(50),
    is_available BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
