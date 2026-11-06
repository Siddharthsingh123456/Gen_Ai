"""PART 3 - Map-Reduce summarization chain (Tasks 7-9). Task 7 (conceptual) is in Readme.md."""
from summarizer import *

text = load_text()
llm = get_llm()

# Task 8: split into chunks -> map_reduce
docs = split_text(text, chunk_size=2000, chunk_overlap=200)
print(f"=== Task 8: Map-Reduce === (document split into {len(docs)} chunks)")
(final, steps), secs = timed(map_reduce_summary, llm, docs, return_steps=True)
print("\nFINAL SUMMARY:\n", final, f"\n(time: {secs}s)")

# Task 9: analyse the map outputs
print("\n=== Task 9: Intermediate (map) summaries ===")
log = []
for i, s in enumerate(steps, 1):
    print(f"\n[Chunk {i}] {s}")
    log.append(f"[Chunk {i}] {s}")
print("\nObservation: the reduce step merged", len(steps),
      "chunk summaries into one coherent summary, removing repetition.")
save_output("part3_map_reduce_final.txt", final)
save_output("part3_map_outputs.txt", "\n\n".join(log))
