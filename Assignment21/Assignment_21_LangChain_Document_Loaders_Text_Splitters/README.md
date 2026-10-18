# Assignment 21 — LangChain Document Loaders & Text Splitters

This project follows the 12 tasks in the TuteDude Assignment 21 brief.

## Important
The project uses the **real LangChain packages**. There are no mock loader/splitter classes.

If you see `REAL LANGCHAIN IMPORT FAILED`, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

## Files

- `main.py` — all 12 tasks with clear task labels and output
- `Assignment_21.ipynb` — notebook with individual task cells
- `data/sample.txt` — text input
- `data/sample.csv` — CSV input
- `data/sample.pdf` — real PDF with visible text generated using ReportLab
- `data/sample.md` — Markdown input for structured splitting
- `outputs/` — place your real run output here
- `MY_RUN_NOTES.txt` — fill this after your own execution
- `requirements.txt` — dependencies

## Notebook
The notebook is intentionally split into individual Task 1–12 sections instead of only calling `main()`. Run all cells after installing the dependencies so Jupyter records the actual outputs.

## Web loader
`WebBaseLoader` uses `https://example.com` as a stable public test page. Network restrictions in a college/lab environment can still block it. If that happens, the script reports the real exception instead of pretending that web extraction succeeded.

## Task 6
Large documents need splitting because LLMs have finite context windows and token limits. Smaller chunks improve retrieval precision and reduce irrelevant context.

## Task 10
Semantic chunking is explained and attempted when the optional experimental package is available. It is not used as a replacement for the required standard splitters.

## Submission
Before submitting, run the notebook and `main.py` yourself and update `MY_RUN_NOTES.txt` with what you actually observed.
