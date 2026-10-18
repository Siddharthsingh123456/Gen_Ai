"""PART 2 - LangChain database engine (Tasks 3 & 4)."""
from sqlalchemy import create_engine, inspect, text
from langchain_community.utilities import SQLDatabase
from config import SQLITE_URI


def task3_sqlalchemy_engine():
    print("=== Task 3: SQLAlchemy engine ===")
    engine = create_engine(SQLITE_URI)                      # 1. create engine
    with engine.connect() as conn:                          # 2. connect to company.db
        conn.execute(text("SELECT 1"))
    print("Connection OK ->", engine.url)
    print("Tables:", inspect(engine).get_table_names())     # 3. fetch table names
    return engine


def task4_langchain_db():
    print("\n=== Task 4: LangChain SQLDatabase ===")
    db = SQLDatabase.from_uri(SQLITE_URI)
    print("Dialect:", db.dialect)
    print("Available tables:", db.get_usable_table_names())
    print("\nSchema information:\n", db.get_table_info())
    print("Sample query:", db.run("SELECT department, COUNT(*) FROM employees GROUP BY department;"))
    return db


if __name__ == "__main__":
    task3_sqlalchemy_engine()
    task4_langchain_db()
