"""PART 4 / 5 - SQL Toolkit, SQL Agent, Chat (Tasks 5-8).

Usage:
    python sql_agent.py --db sqlite            # interactive chat on SQLite
    python sql_agent.py --db mysql             # interactive chat on MySQL Workbench DB
    python sql_agent.py --db both --demo       # run Task 7 + Task 8 questions on both DBs
"""
import argparse
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from config import get_llm, SQLITE_RO_URI, MYSQL_URI

# Safety: instructions + read-only DB connection (SQLite) + no hardcoded SQL anywhere.
SAFETY_PREFIX = """You are an AI Data Assistant for business users who do not know SQL.
You are connected to a {dialect} database. Rules:
- Write SQL dynamically based on the user's question; always inspect tables/schema first.
- ONLY run read-only SELECT queries. NEVER run INSERT, UPDATE, DELETE, DROP, ALTER or CREATE.
- Limit results to at most {top_k} rows unless asked otherwise.
- Always double-check your query before executing it.
- If the question is vague or ambiguous (e.g. 'show me the data', 'who is best?'),
  do NOT guess: reply with a short clarifying question and list the options you see
  (relevant tables/columns).
- Answer in plain business language, not SQL.
"""

TASK7_QUESTIONS = [
    "How many employees are there in each department?",
    "Who has the highest salary?",
    "What is the total sales amount?",
    "What is the average salary per department?",
]

TASK8_QUESTIONS = [          # unclear / ambiguous on purpose
    "Show me the data.",
    "Who is the best employee?",
    "How are we doing?",
]


def build_db(kind: str) -> SQLDatabase:
    if kind == "sqlite":
        return SQLDatabase.from_uri(SQLITE_RO_URI)   # read-only connection
    if kind == "mysql":
        return SQLDatabase.from_uri(MYSQL_URI)       # use a read-only MySQL user in production
    raise ValueError(kind)


def build_agent(db: SQLDatabase):
    llm = get_llm()
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)      # Task 5
    print("Toolkit tools:")                           # built-in tools: query / info / list / checker
    for t in toolkit.get_tools():
        print(f"  - {t.name}: {t.description.splitlines()[0][:90]}")
    return create_sql_agent(                          # Task 6
        llm=llm,
        toolkit=toolkit,
        agent_type="tool-calling",                    # agent chooses tools automatically
        verbose=True,                                 # shows thoughts + generated SQL
        prefix=SAFETY_PREFIX,
        top_k=10,
        handle_parsing_errors=True,
    )


def ask(agent, question: str):
    print(f"\n{'=' * 70}\nQ: {question}\n{'=' * 70}")
    result = agent.invoke({"input": question})
    print(f"\nA: {result['output']}")
    return result["output"]


def run_demo(agent):
    print("\n##### TASK 7: Chat with SQL database #####")
    for q in TASK7_QUESTIONS:
        ask(agent, q)
    print("\n##### TASK 8: Ambiguous queries #####")
    for q in TASK8_QUESTIONS:
        ask(agent, q)


def chat(agent):
    print("Type a question (or 'exit').")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in {"exit", "quit", "q"}:
            break
        if q:
            ask(agent, q)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", choices=["sqlite", "mysql", "both"], default="sqlite")
    p.add_argument("--demo", action="store_true", help="run Task 7 & 8 questions automatically")
    args = p.parse_args()

    targets = ["sqlite", "mysql"] if args.db == "both" else [args.db]
    for target in targets:
        print(f"\n\n################ DATABASE: {target.upper()} ################")
        agent = build_agent(build_db(target))
        run_demo(agent) if args.demo else chat(agent)
