drop database if exists hotels_db;
create database hotels_db;
use hotels_db;

CREATE TABLE hotels (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    rating FLOAT NOT NULL,
    pool BOOLEAN NOT NULL,
    gym BOOLEAN NOT NULL,
    spa BOOLEAN NOT NULL,
    restaurants VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    weddings BOOLEAN NOT NULL,
    conferences BOOLEAN NOT NULL,
    banquets BOOLEAN NOT NULL,
    capacity INT NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE reservations (
  id INT NOT NULL AUTO_INCREMENT,
  guest_name VARCHAR(255) NOT NULL,
  checkin_date DATE NOT NULL,
  checkout_date DATE NOT NULL,
  room_type VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO hotels (name, address, city, country, phone, rating, pool, gym, spa, restaurants, description, price, weddings, conferences, banquets, capacity) VALUES
    ('The Grand Hotel', '123 Main St', 'New York', 'USA', '+1-212-555-1234', 4.5, TRUE, TRUE, TRUE, 'Italian, French, Japanese', '', 0, FALSE, FALSE, FALSE, 0),
    ('The Ritz-Carlton', '1 Central Park West', 'New York', 'USA', '+1-212-555-5678', 5.0, TRUE, TRUE, TRUE, 'American, French, Seafood', '', 0, FALSE, FALSE, FALSE, 0),
    ('The Plaza', '768 5th Ave', 'New York', 'USA', '+1-212-555-9100', 4.0, FALSE, TRUE, TRUE, 'European, Asian', '', 0, FALSE, FALSE, FALSE, 0),
    ('The Mandarin Oriental', '80 Columbus Cir', 'New York', 'USA', '+1-212-555-4321', 4.8, TRUE, TRUE, TRUE, 'Chinese, French, Japanese', 'Spacious room with a king-size bed and a view of Central Park', 600, TRUE, TRUE, TRUE, 300),
    ('The Fairmont', '950 Mason St', 'San Francisco', 'USA', '+1-415-555-1234', 4.3, TRUE, TRUE, FALSE, 'American, French, Japanese', '', 0, FALSE, FALSE, FALSE, 0);

INSERT INTO reservations (guest_name, checkin_date, checkout_date, room_type) VALUES
('John Doe', '2023-04-25', '2023-04-30', 'Deluxe Room'),
('Jane Smith', '2023-05-01', '2023-05-05', 'Standard Room'),
('Alice Lee', '2023-05-10', '2023-05-15', 'Suite'),
('Bob Johnson', '2023-05-20', '2023-05-23', 'Deluxe Room'),
('Samantha Brown', '2023-06-01', '2023-06-05', 'Standard Room'),
('David Kim', '2023-06-10', '2023-06-15', 'Deluxe Room'),
('Maria Perez', '2023-06-20', '2023-06-22', 'Suite'),
('Alex Wong', '2023-06-25', '2023-06-30', 'Standard Room');

