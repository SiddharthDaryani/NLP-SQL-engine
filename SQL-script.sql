-- 1. Create the database
CREATE DATABASE IF NOT EXISTS tshirt_store;
USE tshirt_store;

-- 2. Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL,
    size VARCHAR(10) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    sku VARCHAR(50),
    UNIQUE KEY unique_product (name, color, size)
);

-- 3. Insert data
INSERT INTO products (name, color, size, price, quantity, description, is_active, sku)
VALUES
('Classic Tee', 'Blue', 'XL', 19.99, 25, 'A classic blue t-shirt in XL size.', 1, 'CT-BL-XL'),
('Classic Tee', 'Red', 'L', 18.99, 15, 'A classic red t-shirt in L size.', 1, 'CT-RD-L'),
('Classic Tee', 'Green', 'M', 17.99, 10, 'A classic green t-shirt in M size.', 1, 'CT-GR-M'),
('V-Neck', 'Black', 'S', 20.99, 8, 'Stylish black V-neck t-shirt in S size.', 1, 'VN-BK-S'),
('V-Neck', 'White', 'M', 20.99, 12, 'White V-neck t-shirt in M size.', 1, 'VN-WH-M'),
('Graphic Tee', 'Blue', 'L', 22.99, 5, 'Blue graphic t-shirt in L size.', 1, 'GT-BL-L');