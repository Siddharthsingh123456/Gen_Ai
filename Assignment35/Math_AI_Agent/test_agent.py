"""Task 2 tests. Part A tests the tools offline; Part B runs the real agent on sample problems.
Run:  python test_agent.py          (Part B needs an LLM key / Ollama)"""
from math_tools import safe_calculate, solve_equation

print("=== Part A: tool tests (no LLM needed) ===")
checks = [
    ("calculator", "12*(3+4)", "84"),
    ("calculator", "15/100*240", "36"),
    ("calculator", "80*(1-25/100)", "60"),
    ("calculator", "(250-200)/200*100", "25"),
    ("calculator", "10/0", "Error: division by zero"),
]
for _, expr, expected in checks:
    got = safe_calculate(expr)
    print(f"{'PASS' if got == expected else 'FAIL'}  {expr} = {got}")
print("solve 2*x + 5 = 17  ->", solve_equation.invoke("2*x + 5 = 17"))
print("solve x**2 - 5x + 6 = 0 ->", solve_equation.invoke("x**2 - 5*x + 6 = 0"))
print("blocked injection ->", safe_calculate("__import__('os').system('ls')"))

QUESTIONS = {
    "Arithmetic word problem": "Riya bought 7 notebooks at 45 rupees each and 3 pens at 12 rupees each. How much did she spend in total?",
    "Percentage problem": "A phone costs 20000 rupees. After a 15% discount, what is the price? Also what is the discount amount?",
    "Simple algebra": "Solve for x: 3x + 7 = 25",
}

if __name__ == "__main__":
    from math_agent import build_agent, solve
    print("\n=== Part B: agent tests ===")
    agent, chat = build_agent(), []
    for title, q in QUESTIONS.items():
        ans, steps = solve(agent, q, chat)
        print(f"\n[{title}] {q}")
        for s in steps:
            print(f"  tool: {s['tool']}({s['input']}) -> {s['output']}")
        print("  Agent:", ans)
        chat += [{"role": "user", "content": q}, {"role": "assistant", "content": ans}]
    q = "Now multiply the last answer by 2"
    ans, _ = solve(agent, q, chat)
    print(f"\n[Memory test] {q}\n  Agent:", ans)
