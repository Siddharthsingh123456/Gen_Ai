-- PART 3: Run this script in MySQL Workbench (File > Open SQL Script > Execute)
CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INT
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    employee_id INT,
    amount INT,
    sale_date VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

INSERT INTO employees VALUES
(1,'Aarav Sharma','Sales',65000),(2,'Priya Verma','Sales',72000),
(3,'Rohan Gupta','Engineering',120000),(4,'Sneha Iyer','Engineering',135000),
(5,'Vikram Singh','Engineering',110000),(6,'Anita Desai','HR',58000),
(7,'Karan Mehta','HR',61000),(8,'Neha Kapoor','Marketing',70000),
(9,'Rahul Nair','Marketing',68000),(10,'Divya Rao','Finance',95000),
(11,'Manish Tiwari','Finance',88000),(12,'Pooja Joshi','Sales',60000);

INSERT INTO sales VALUES
(1,1,15000,'2024-01-05'),(2,2,22000,'2024-01-12'),(3,1,18000,'2024-02-03'),
(4,12,9000,'2024-02-14'),(5,2,30000,'2024-02-20'),(6,12,12500,'2024-03-02'),
(7,1,27000,'2024-03-15'),(8,2,19500,'2024-03-28'),(9,12,8000,'2024-04-09'),
(10,1,21000,'2024-04-21'),(11,2,16000,'2024-05-07'),(12,12,14000,'2024-05-19');

SELECT * FROM employees;
SELECT * FROM sales;
