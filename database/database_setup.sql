-- Drop tables if they already exist (for resetting in DB Fiddle)
DROP TABLE IF EXISTS System_Logs;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Transaction_Categories;
DROP TABLE IF EXISTS Users;

-- 1. Users Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,   -- Unique ID for each user
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- 2. Transaction Categories Table
CREATE TABLE Transaction_Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 3. Transactions Table
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    
    -- Foreign Keys
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES Users(user_id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
);

-- 4. System Logs Table
CREATE TABLE System_Logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,

    CONSTRAINT fk_transaction FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
);

-- -- Insert Sample Users
-- INSERT INTO Users (name, phone_number, email) VALUES
-- ('Alice Johnson', '250700111222', 'alice@example.com'),
-- ('Bob Smith', '250700333444', 'bob@example.com'),
-- ('Carol Danvers', '250700555666', 'carol@example.com');

-- -- Insert Sample Categories
-- INSERT INTO Transaction_Categories (category_name, description) VALUES
-- ('Transfer', 'Money sent between users'),
-- ('Airtime', 'Mobile top-up purchase'),
-- ('Bill Payment', 'Utility bill settlements');

-- -- Insert Sample Transactions
-- INSERT INTO Transactions (sender_id, receiver_id, category_id, amount, status) VALUES
-- (1, 2, 1, 1500.00, 'completed'),
-- (2, 3, 2, 500.00, 'completed'),
-- (1, 3, 3, 3000.00, 'pending');

-- -- Insert Sample Logs
-- INSERT INTO System_Logs (transaction_id, message) VALUES
-- (1, 'Transaction processed successfully'),
-- (2, 'Airtime delivered'),
-- (3, 'Pending approval for bill payment');