# Assignment 34: Text Summarization using LangChain

Four summarization strategies built with LangChain + an LLM of your choice
(OpenAI / Groq / Ollama). No fine-tuning is used.

## Dataset
`data/article.txt` – a long article, *"The Rise of Renewable Energy"*
(about 11,800 characters, 1,800 words, roughly 4-5 pages). It is split into 7 chunks
for the map-reduce and refine chains. A PDF also works: set `DOC_PATH=your.pdf` in `.env`.

## Project structure
| File | Covers |
|------|--------|
| `summarizer.py` | Shared code: LLM factory, loaders, splitter, prompts, the 4 strategies |
| `part1_prompt_summary.py` | Part 1 – Tasks 1-3 (PromptTemplate, short vs bullet summary) |
| `part2_stuff_chain.py` | Part 2 – Tasks 5-6 (stuff chain + comparison with prompt-based) |
| `part3_map_reduce.py` | Part 3 – Tasks 8-9 (map-reduce + intermediate chunk summaries) |
| `part4_refine.py` | Part 4 – Tasks 11-12 (refine chain + comparison of all methods, saved to `outputs/comparison.md`) |
| `part5_mini_project.py` | Part 5 – Task 13 `summarize_document(text, method)` with prompt / stuff / map_reduce / refine |
| `Readme.md` | Conceptual answers (Tasks 4, 7, 10, 14) and comparison notes |

## How to run
```bash
pip install -r requirements.txt
cp .env.example .env                 # add your API key (or choose ollama)

python part1_prompt_summary.py
python part2_stuff_chain.py
python part3_map_reduce.py
python part4_refine.py
python part5_mini_project.py --method map_reduce     # prompt | stuff | map_reduce | refine
```
All generated summaries are saved in the `outputs/` folder.

Note: on free API tiers (e.g. Groq) a per-minute token limit may stop the run.
If you hit it, wait a minute, or lower `chunk_size`, or use `LLM_PROVIDER=ollama`.

---

## PART 2 – Stuff chain

**Task 4 – Why is a stuff chain needed?**
1. *What is it?* The simplest chain: all documents are "stuffed" into a single prompt
   and the LLM summarizes them in one call.
2. *When is it suitable?* When the whole document fits comfortably in the model's context
   window: short or medium articles, emails, single-page reports.
3. *Limitations:* Fails or truncates when the text exceeds the context window; cost and
   latency grow with prompt size; models may overlook details in the middle of very long
   prompts ("lost in the middle"); no way to handle documents of unlimited length.

**Task 6 – Prompt-based vs Stuff chain**
Both send the entire text in one request, so quality is usually very similar.
The difference is engineering: `load_summarize_chain("stuff")` works with `Document`
objects, is reusable and plugs in with the other chain types, while a bare PromptTemplate
gives you maximum control over wording and format. Both share the same limit: the document
must fit in the context window.

## PART 3 – Map-Reduce

**Task 7 – Why map-reduce?**
1. Large documents do not fit into one prompt, and even when they do, quality drops on
   very long inputs. Map-reduce splits the problem into small pieces the model handles well.
2. *Map:* each chunk is summarized independently (these calls can run in parallel).
   *Reduce:* the chunk summaries are combined in a final call into one coherent summary.
   If the combined summaries are still too long, they are collapsed recursively.

**Task 9 – Observation of map outputs**
Each chunk summary captures only the local topic (e.g. history, economics, storage, grid,
policy). The reduce step merges them, removes repeated points and restores the overall
flow. Weakness: chunks are summarized without knowing each other, so cross-chunk
connections can be lost.

## PART 4 – Refine

**Task 10 – Understanding the refine chain**
1. *How it works:* summarize chunk 1; then, for every next chunk, send
   "existing summary + new chunk" to the LLM and ask it to refine the summary.
   The summary evolves step by step through the document.
2. *Difference from map-reduce:* map-reduce is parallel and chunks are independent;
   refine is sequential, each step depends on the previous result. Refine keeps
   context and narrative continuity, but is slower and cannot be parallelized.

**Task 12 – Comparison of all methods** (running `part4_refine.py` produces real numbers
and outputs in `outputs/comparison.md`; the table below is the typical behaviour)

| Method | Summary quality | Coherence | Long-document suitability | LLM calls |
|--------|-----------------|-----------|---------------------------|-----------|
| Prompt-based | Good on short text; general | High | Poor, limited by context | 1 |
| Stuff chain | Same as prompt-based | High | Poor, limited by context | 1 |
| Map-reduce | Good coverage, may miss cross-chunk links | Good (made by reduce) | Very good, scalable, parallel | N + 1 |
| Refine | Often most detailed and context-aware | Very good narrative flow | Good, but slow; early content can be diluted or over-weighted | N |

## PART 5 – Mini project

**Task 13:** `summarize_document(text, method="map_reduce")` in `part5_mini_project.py`
switches between `prompt`, `stuff`, `map_reduce` and `refine`.

**Task 14 – Observations & insights**
1. *Best strategy for very long documents:* map-reduce, because it scales to any length,
   makes calls that can run in parallel and never exceeds the context window. For
   extremely long texts, a hierarchical (recursive) map-reduce is used. Refine is a
   good alternative when narrative order matters (stories, transcripts).
2. *Trade-offs between speed and quality:* prompt/stuff are the fastest and cheapest
   (one call) but only work for shorter text. Map-reduce is a good balance:
   N+1 calls but parallelizable. Refine usually gives the most coherent, context-aware
   summary but is the slowest (N sequential calls) and costs the most. Smaller chunks
   give more detail but more calls; larger chunks are faster but may lose detail.
