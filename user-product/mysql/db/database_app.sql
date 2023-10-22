USE app;

-- Schema for the User table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    location VARCHAR(255),
    preferences VARCHAR(255)
);

-- Schema for the Product table
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    category VARCHAR(255),
    Product_name VARCHAR(255),
    description TEXT,
    tags VARCHAR(255)
);

-- Schema for the Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert statements for the User table
INSERT INTO users (user_id, name, age, gender, location, preferences) VALUES
(1, 'Alice', 30, 'Female', 'New York', 'Electronics'),
(2, 'Bob', 25, 'Male', 'Los Angeles', 'Clothing'),
(3, 'Charlie', 35, 'Male', 'San Francisco', 'Sports'),
(4, 'David', 28, 'Male', 'Chicago', 'Books'),
(5, 'Eve', 22, 'Female', 'Miami', 'Food');

-- Insert statements for the Product table
INSERT INTO products (product_id, category, Product_name, description, tags) VALUES
(101, 'Electronics', 'Smartphone Galaxy S22', 'The latest Galaxy smartphone with 5G support, AMOLED display, and advanced camera features.', 'Smartphone, Samsung, 5G, AMOLED, Camera'),
(103, 'Sports', 'Running Shoes UltraBoost', 'High-performance running shoes with responsive cushioning and adaptive knit upper.', 'Running Shoes, Adidas, Athletic, Cushioning'),
(102, 'Electronics', 'Laptop ProBook X360', 'A versatile laptop with a 360-degree hinge, powerful performance, and long-lasting battery.', 'Laptop, HP, 2-in-1, Performance'),
(104, 'Books', 'Book: "The Great Gatsby"', 'A classic novel by F. Scott Fitzgerald exploring the decadence of the 1920s.', 'Book, Literature, Classic, 1920s'),
(105, 'Electronics', 'Bluetooth Speaker SoundWave', 'Portable Bluetooth speaker with 360-degree sound, built-in microphone, and waterproof design.', 'Speaker, Bluetooth, Waterproof, Portable');

-- Insert statements for the Transactions table
INSERT INTO transactions (transaction_id, user_id, product_id) VALUES
(1, 1, 101),
(2, 1, 103),
(3, 2, 102),
(4, 2, 104),
(5, 3, 103),
(6, 3, 104),
(7, 4, 101),
(8, 4, 102),
(9, 5, 105);
