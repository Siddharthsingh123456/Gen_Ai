"""PART 4 - Refine chain (Tasks 10-12). Task 10 (conceptual) is in Readme.md."""
from summarizer import *

text = load_text()
llm = get_llm()
docs = split_text(text, chunk_size=2000, chunk_overlap=200)

# Task 11: refine chain (iterative)
print(f"=== Task 11: Refine chain === ({len(docs)} chunks)")
(refined, steps), t_refine = timed(refine_summary, llm, docs, return_steps=True)
for i, s in enumerate(steps, 1):
    print(f"\n[After chunk {i}] {s}")
print("\nFINAL REFINED SUMMARY:\n", refined)
save_output("part4_refine_summary.txt", refined)

# Task 12: comparison of ALL methods -> outputs/comparison.md
print("\n=== Task 12: Comparison of all methods ===")
results = {}
results["Prompt-based"] = timed(prompt_summary, llm, text, SHORT_PROMPT)
results["Stuff chain"] = timed(stuff_summary, llm, [Document(page_content=text)])
results["Map-reduce"] = timed(map_reduce_summary, llm, docs)
results["Refine"] = (refined, t_refine)

md = ["# Comparison of Summarization Methods\n",
      "| Method | Words | Time (s) | LLM calls |", "|---|---|---|---|"]
calls = {"Prompt-based": 1, "Stuff chain": 1, "Map-reduce": f"{len(docs)}+1", "Refine": len(docs)}
for name, (out, secs) in results.items():
    md.append(f"| {name} | {len(out.split())} | {secs} | {calls[name]} |")
md.append("")
for name, (out, _) in results.items():
    md.append(f"## {name}\n{out}\n")
report = "\n".join(md)
print(report)
save_output("comparison.md", report)
print("\nNow judge: summary quality, coherence, suitability for long documents (see Readme.md).")
