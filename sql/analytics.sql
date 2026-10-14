-- PostgreSQL schema for cleaned_sales.csv exported by src/analyze.py
-- Load via psql \copy, a database client, or a notebook. Quote case-sensitive columns in import mappings.
CREATE TABLE IF NOT EXISTS sales_lines (
    invoice_no TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT,
    quantity NUMERIC NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    unit_price NUMERIC NOT NULL,
    customer_id TEXT,
    country TEXT,
    sales_amount NUMERIC NOT NULL,
    month TEXT NOT NULL
);
-- Monthly revenue and order volume
SELECT month, ROUND(SUM(sales_amount),2) AS revenue,
       COUNT(DISTINCT invoice_no) AS orders,
       SUM(quantity) AS units
FROM sales_lines GROUP BY month ORDER BY month;

-- Top ten products
SELECT stock_code, description, ROUND(SUM(sales_amount),2) AS revenue,
       SUM(quantity) AS units
FROM sales_lines GROUP BY stock_code, description
ORDER BY revenue DESC LIMIT 10;

-- Customer repeat-order frequency (known customers only)
WITH customer_orders AS (
 SELECT customer_id, COUNT(DISTINCT invoice_no) AS order_count
 FROM sales_lines WHERE customer_id IS NOT NULL
 GROUP BY customer_id
)
SELECT COUNT(*) AS identified_customers,
       COUNT(*) FILTER (WHERE order_count > 1) AS repeat_customers
FROM customer_orders;

-- Revenue by country
SELECT country, ROUND(SUM(sales_amount),2) AS revenue
FROM sales_lines GROUP BY country ORDER BY revenue DESC;
