"""Math tools used by the agent: a safe calculator and an algebra equation solver."""
import ast
import math
import operator as op
from langchain_core.tools import tool

# ---- safe expression evaluator (no eval() on raw text) ----
_BIN = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv, ast.Mod: op.mod, ast.Pow: op.pow}
_UNARY = {ast.UAdd: op.pos, ast.USub: op.neg}
_FUNCS = {"sqrt": math.sqrt, "abs": abs, "round": round, "log": math.log,
          "log10": math.log10, "sin": math.sin, "cos": math.cos, "tan": math.tan,
          "min": min, "max": max}
_CONSTS = {"pi": math.pi, "e": math.e}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("exponent too large")
        return _BIN[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Name) and node.id in _CONSTS:
        return _CONSTS[node.id]
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in _FUNCS and not node.keywords):
        return _FUNCS[node.func.id](*[_eval(a) for a in node.args])
    raise ValueError("unsupported expression")


def safe_calculate(expression: str) -> str:
    expr = expression.strip().replace("^", "**").replace("×", "*").replace("÷", "/").replace(",", "")
    # allow "20%" style input -> (20/100)
    expr = expr.replace("%", "/100")
    try:
        result = _eval(ast.parse(expr, mode="eval").body)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as exc:
        return f"Error: could not evaluate '{expression}' ({exc})"
    if isinstance(result, float):
        result = round(result, 10)
        if result.is_integer():
            result = int(result)
    return str(result)


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression and return the numeric result.
    Supports + - * / ** % (percent), parentheses, sqrt(), abs(), round(), log(), pi.
    Examples: '12*(3+4)', '15/100*80', 'sqrt(144)', '(250-200)/200*100'."""
    return safe_calculate(expression)


@tool
def solve_equation(equation: str) -> str:
    """Solve a simple algebra equation for its variable(s).
    Use '=' between both sides, e.g. '2*x + 5 = 17' or 'x**2 - 5*x + 6 = 0'.
    Returns the solution(s)."""
    import sympy as sp
    from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                            implicit_multiplication_application)
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        text = equation.replace("^", "**")
        if "=" in text:
            left, right = text.split("=", 1)
            expr = parse_expr(left, transformations=transformations) - parse_expr(right, transformations=transformations)
        else:
            expr = parse_expr(text, transformations=transformations)
        symbols = sorted(expr.free_symbols, key=lambda s: s.name)
        if not symbols:
            return "Error: no variable found in the equation"
        sol = sp.solve(expr, symbols)
        return f"{', '.join(map(str, symbols))} = {sol}"
    except Exception as exc:
        return f"Error: could not solve '{equation}' ({exc})"


TOOLS = [calculator, solve_equation]
