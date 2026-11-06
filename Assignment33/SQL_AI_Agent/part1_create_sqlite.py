"""PART 1 - Storing data in a SQLite database (Tasks 1 & 2)."""
import os
import sqlite3
from config import SQLITE_PATH

SCHEMA = """
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
);
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    amount INTEGER,
    sale_date TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
"""

EMPLOYEES = [
    (1, "Aarav Sharma", "Sales", 65000),
    (2, "Priya Verma", "Sales", 72000),
    (3, "Rohan Gupta", "Engineering", 120000),
    (4, "Sneha Iyer", "Engineering", 135000),
    (5, "Vikram Singh", "Engineering", 110000),
    (6, "Anita Desai", "HR", 58000),
    (7, "Karan Mehta", "HR", 61000),
    (8, "Neha Kapoor", "Marketing", 70000),
    (9, "Rahul Nair", "Marketing", 68000),
    (10, "Divya Rao", "Finance", 95000),
    (11, "Manish Tiwari", "Finance", 88000),
    (12, "Pooja Joshi", "Sales", 60000),
]

SALES = [
    (1, 1, 15000, "2024-01-05"),
    (2, 2, 22000, "2024-01-12"),
    (3, 1, 18000, "2024-02-03"),
    (4, 12, 9000, "2024-02-14"),
    (5, 2, 30000, "2024-02-20"),
    (6, 12, 12500, "2024-03-02"),
    (7, 1, 27000, "2024-03-15"),
    (8, 2, 19500, "2024-03-28"),
    (9, 12, 8000, "2024-04-09"),
    (10, 1, 21000, "2024-04-21"),
    (11, 2, 16000, "2024-05-07"),
    (12, 12, 14000, "2024-05-19"),
]


def create_database():
    if os.path.exists(SQLITE_PATH):
        os.remove(SQLITE_PATH)
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    cur.executemany("INSERT INTO employees VALUES (?,?,?,?)", EMPLOYEES)
    cur.executemany("INSERT INTO sales VALUES (?,?,?,?)", SALES)
    conn.commit()
    return conn


def verify(conn):
    cur = conn.cursor()
    print("=== Verification queries ===")
    for table in ("employees", "sales"):
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"Rows in {table}: {cur.fetchone()[0]}")
    checks = {
        "All employees": "SELECT * FROM employees",
        "Highest salary": "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 1",
        "Total sales amount": "SELECT SUM(amount) FROM sales",
        "Employees per department": "SELECT department, COUNT(*) FROM employees GROUP BY department",
    }
    for title, q in checks.items():
        print(f"\n-- {title}\n   {q}")
        for row in cur.execute(q).fetchall():
            print("  ", row)


if __name__ == "__main__":
    connection = create_database()
    verify(connection)
    connection.close()
    print(f"\nDatabase created at: {SQLITE_PATH}")
