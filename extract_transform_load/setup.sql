--for orders table

CREATE SCHEMA IF NOT EXISTS orders_db;
CREATE TABLE orders_db.orders (
 order_id SERIAL PRIMARY KEY,
 customer_name TEXT,
 product_id INT,
 quantity INT,
 order_date DATE,
 status TEXT -- 'completed', 'pending', 'cancelled'
);
INSERT INTO orders_db.orders
 (customer_name, product_id, quantity, order_date, status)
VALUES
 ('Alice', 101, 2, '2024-01-10', 'completed'),
 ('Bob', 102, 1, '2024-01-11', 'cancelled'),
 ('Alice', 103, 5, '2024-01-12', 'completed'),
 ('Charlie', 101, 3, '2024-01-13', 'pending'),
 ('Bob', 101, 1, '2024-01-14', 'completed');

--for products table

CREATE SCHEMA IF NOT EXISTS products_db;
CREATE TABLE products_db.products (
 product_id INT PRIMARY KEY,
 product_name TEXT,
 category TEXT,
 unit_price NUMERIC(10,2)
);
INSERT INTO products_db.products VALUES
 (101, 'Wireless Mouse', 'Electronics', 25.99),
 (102, 'Desk Lamp', 'Furniture', 45.00),
 (103, 'Notebook (Pack 5)', 'Stationery', 8.50);

--for target db (analytics_db)

CREATE SCHEMA IF NOT EXISTS analytics_db;
CREATE TABLE analytics_db.sales_summary (
 order_id INT,
 customer_name TEXT,
 product_name TEXT,
 category TEXT,
 quantity INT,
 unit_price NUMERIC(10,2),
 total_amount NUMERIC(10,2), -- quantity * unit_price
 order_date DATE,
 order_month TEXT, -- e.g. '2024-01'
 status TEXT
);