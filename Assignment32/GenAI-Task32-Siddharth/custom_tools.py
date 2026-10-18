"""PART 2 - Tasks 3 & 4: custom tools and a custom toolkit.

Every tool takes ONE string input so it works both with native tool calling (bind_tools)
and with the text-based ReAct loop.

Run:  python custom_tools.py         (tests every tool independently - no LLM needed)
"""
import ast
import operator
import sqlite3
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from langchain_core.tools import BaseTool, tool

# =====================================================================================
# Task 3: custom tool  - company_policy_lookup (mock data is fine)
# =====================================================================================
POLICIES = {
    "leave": "Full-time employees get 24 days of paid annual leave per year; up to 10 unused days carry forward. "
             "Sick leave is 12 days per year.",
    "remote work": "Hybrid model: 3 office days per week (Tue-Thu); remote on Monday and Friday. "
                   "Home-office allowance: Rs 15,000 one time.",
    "working hours": "Standard hours are 10:00 to 18:30, Monday to Friday. Core hours are 11:00 to 16:00.",
    "expenses": "Expense claims must be filed within 30 days with receipts. Hotel limit: Rs 6,000/night in metro cities.",
    "learning": "Every employee gets an annual learning budget of Rs 30,000 for courses and certifications.",
    "notice period": "Notice period is 60 days for confirmed employees and 30 days during probation.",
}


@tool
def company_policy_lookup(query: str) -> str:
    """Returns company policy information. Input: a topic such as 'leave', 'remote work',
    'working hours', 'expenses', 'learning' or 'notice period'."""
    q = query.lower()
    matches = [f"{topic}: {text}" for topic, text in POLICIES.items()
               if topic in q or any(word in q for word in topic.split() if len(word) > 3)]
    if matches:
        return "\n".join(matches)
    return f"No policy found for '{query}'. Available topics: {', '.join(POLICIES)}."


# =====================================================================================
# Task 2 (calculator) / Task 4 (toolkit): safe calculator
# =====================================================================================
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only numbers and + - * / // % ** ( ) are allowed")


@tool
def calculator(expression: str) -> str:
    """Evaluates a math expression, e.g. '(24 - 10) * 3 + 2**5'. Use it for ANY arithmetic.
    Input: only numbers and + - * / // % ** and parentheses."""
    try:
        result = _eval(ast.parse(expression.strip().replace("^", "**"), mode="eval").body)
        return str(round(result, 6) if isinstance(result, float) else result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as e:
        return f"Error: could not evaluate '{expression}' ({e})"


# =====================================================================================
# Task 4: toolkit members - simple database query + date/time
# =====================================================================================
def _make_db() -> sqlite3.Connection:
    """Tiny in-memory employee database (mock data)."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute("CREATE TABLE employees (name TEXT, department TEXT, role TEXT, leave_balance INTEGER)")
    conn.executemany("INSERT INTO employees VALUES (?,?,?,?)", [
        ("Asha Verma", "Engineering", "Backend Developer", 14),
        ("Rohan Mehta", "Engineering", "ML Engineer", 9),
        ("Priya Nair", "Engineering", "Frontend Developer", 20),
        ("Kabir Singh", "HR", "HR Manager", 11),
        ("Neha Kapoor", "HR", "Recruiter", 17),
        ("Vikram Rao", "Finance", "Accountant", 6),
    ])
    return conn


_DB = _make_db()


@tool
def employee_database_query(department: str) -> str:
    """Looks up employees of a department in the company database and returns name, role and
    remaining leave days. Input: a department name: 'Engineering', 'HR' or 'Finance'."""
    rows = _DB.execute(
        "SELECT name, role, leave_balance FROM employees WHERE lower(department) = lower(?)",
        (department.strip(),),                       # parameterised query: no SQL injection
    ).fetchall()
    if not rows:
        return f"No employees found for department '{department}'. Departments: Engineering, HR, Finance."
    return "\n".join(f"{n} - {r} - {b} leave days left" for n, r, b in rows)


@tool
def get_current_datetime(timezone_name: str = "Asia/Kolkata") -> str:
    """Returns the current date and time. Input: an IANA time zone such as 'Asia/Kolkata' or 'UTC'
    (any other input falls back to UTC)."""
    name = timezone_name.strip().strip("'\"") or "UTC"
    try:
        tz = ZoneInfo(name)
    except Exception:
        tz, name = ZoneInfo("UTC"), "UTC"
    return datetime.now(tz).strftime(f"%A, %d %B %Y, %H:%M:%S ({name})")


# =====================================================================================
# Task 4: Toolkit - groups several tools together
# =====================================================================================
class CompanyToolkit:
    """A small toolkit that groups the company-related tools."""

    def get_tools(self) -> List[BaseTool]:
        return [company_policy_lookup, employee_database_query, get_current_datetime, calculator]


if __name__ == "__main__":
    print("Tools in the toolkit:", [t.name for t in CompanyToolkit().get_tools()], "\n")
    tests = [
        (company_policy_lookup, "leave"),
        (company_policy_lookup, "stock options"),
        (employee_database_query, "Engineering"),
        (employee_database_query, "Marketing"),
        (get_current_datetime, "Asia/Kolkata"),
        (calculator, "(24 - 10) * 3 + 2**5"),
        (calculator, "10 / 0"),
        (calculator, "__import__('os').system('ls')"),
    ]
    for t, arg in tests:
        print(f"[{t.name}]  input={arg!r}\n  -> {t.invoke(arg)}\n")
