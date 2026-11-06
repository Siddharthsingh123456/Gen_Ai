"""PART 3 - Connect Python / LangChain to the MySQL Workbench (MySQL Server) database.

Step 1 (Workbench): create the DB by running mysql_setup.sql, OR run this file
        with `python part3_mysql_workbench.py --setup` to do the same from code.
Step 2 (Code):      this script connects through SQLAlchemy + PyMySQL.
"""
import sys
from sqlalchemy import create_engine, inspect, text
from langchain_community.utilities import SQLDatabase
from config import MYSQL_SERVER_URI, MYSQL_URI, MYSQL_DB
import os


def setup_from_code():
    sql = open(os.path.join(os.path.dirname(__file__), "mysql_setup.sql")).read()
    engine = create_engine(MYSQL_SERVER_URI)
    with engine.begin() as conn:
        for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
            if stmt.upper().startswith("SELECT"):
                continue
            conn.exec_driver_sql(stmt)
    print("MySQL database created from mysql_setup.sql")


def connect():
    engine = create_engine(MYSQL_URI)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"Connected to MySQL database '{MYSQL_DB}'")
    print("Tables:", inspect(engine).get_table_names())
    db = SQLDatabase.from_uri(MYSQL_URI)
    print("LangChain sees:", db.get_usable_table_names())
    print(db.run("SELECT department, COUNT(*) FROM employees GROUP BY department;"))
    return db


if __name__ == "__main__":
    if "--setup" in sys.argv:
        setup_from_code()
    connect()
