"""PART 2 - Stuff summarization chain (Tasks 4-6). Task 4 (conceptual) is answered in Readme.md."""
from summarizer import *

text = load_text()
llm = get_llm()

# Task 5: whole document as ONE Document -> stuff chain
docs = [Document(page_content=text)]
print("=== Task 5: Stuff chain summary ===")
stuff, t_stuff = timed(stuff_summary, llm, docs)
print(stuff)
print(f"\n(time: {t_stuff}s)")
save_output("part2_stuff_summary.txt", stuff)

# Task 6: comparison with the prompt-based summary
prompt_based, t_prompt = timed(prompt_summary, llm, text, SHORT_PROMPT)
print("\n=== Task 6: Prompt-based vs Stuff chain ===")
print(f"Prompt-based : {len(prompt_based.split())} words, {t_prompt}s")
print(f"Stuff chain  : {len(stuff.split())} words, {t_stuff}s")
print("\n--- Prompt-based ---\n", prompt_based)
print("\n--- Stuff chain ---\n", stuff)
