"""TASK 3 - Code assistant features: generation, explanation, bug fixing, optimization."""
from code_assistant import explain_code, fix_bug, generate_code, optimize_code

BUGGY = """def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(average([]))
"""
SLOW = """def has_duplicates(items):
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                return True
    return False
"""

def show(title, text):
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}\n{text}")

show("1. CODE GENERATION: 'a function that checks if a string is a palindrome'",
     generate_code("A function that checks if a string is a palindrome, ignoring case and spaces"))
show("2. CODE EXPLANATION", explain_code(SLOW))
show("3. BUG FIXING (ZeroDivisionError)", fix_bug(BUGGY, "ZeroDivisionError: division by zero"))
show("4. CODE OPTIMIZATION SUGGESTIONS", optimize_code(SLOW))
