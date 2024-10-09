-- Create the database 'store'
CREATE DATABASE store;

-- Use the 'store' database
USE store;

-- Create the 'inventory' table
CREATE TABLE inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    stock INT NOT NULL
);

-- Create the 'sales' table
CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);

-- Create the 'returns' table
CREATE TABLE returns (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    return_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);
