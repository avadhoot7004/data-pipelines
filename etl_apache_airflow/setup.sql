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

--to avoid duplicates when python script is re-run

ALTER TABLE analytics_db.sales_summary
ADD CONSTRAINT sales_summary_order_id_unique
UNIQUE(order_id);

--customer aggregation table
CREATE TABLE analytics_db.customer_totals (
    customer_name TEXT,
    total_spend NUMERIC(10,2),
    order_count INT
);

--end of previous sql

--adding ingested_at column to track when data was ingested
ALTER TABLE analytics_db.sales_summary
ADD COLUMN ingested_at TIMESTAMP DEFAULT NOW();

--adding unique constraint on order_id so duplicates are rejected automatically 
ALTER TABLE analytics_db.sales_summary 
    ADD CONSTRAINT IF NOT EXISTS uq_sales_order_id UNIQUE (order_id); 

--to check idempotency before and after running the dag multiple times
SELECT COUNT(*)
FROM analytics_db.sales_summary; --should return same count even if we run the dag multiple times without changes to source data


