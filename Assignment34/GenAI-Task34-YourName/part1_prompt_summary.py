"""PART 1 - Basic text summarization with PromptTemplate (Tasks 1-3)."""
from summarizer import *

# Task 1: load and prepare
text = load_text()
print("=== Task 1: Document info ===")
print("Total characters:", len(text))
print("Total words     :", len(text.split()))
print("Sample preview  :\n", text[:500], "...\n")

llm = get_llm()

# Task 2: prompt-based summary (system role + {text} placeholder)
print("=== Task 2: Prompt-based summary ===")
summary = prompt_summary(llm, text, SHORT_PROMPT)
print(summary)
save_output("part1_prompt_summary.txt", summary)

# Task 3: prompt variations
print("\n=== Task 3: Prompt variations ===")
short = prompt_summary(llm, text, SHORT_PROMPT)
bullets = prompt_summary(llm, text, BULLET_PROMPT)
print("--- Short summary (5-6 lines) ---\n", short)
print("\n--- Bullet-point summary ---\n", bullets)
print("\nComparison -> words: short =", len(short.split()), "| bullets =", len(bullets.split()))
save_output("part1_variations.txt", f"SHORT:\n{short}\n\nBULLETS:\n{bullets}\n")
