# Assignment 25 — Prompting & LangChain Chains

## Tasks included

1. PromptTemplate with system instruction, user placeholder, dynamic input and multiple tests
2. ChatPromptTemplate + SystemMessage/HumanMessage templates
3. Pydantic output schema with answer, confidence and source
4. Validation and error handling
5. Simple chain: Prompt → LLM → Output
6. Conditional chain
7. Parallel chain
8. Runnables + LCEL
9. LCEL-based RAG chain
10. Observations and insights

## Setup

Create a virtual environment and install:

```bash
python -m pip install -r requirements.txt
```

Set your OpenAI key.

PowerShell:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY"
$env:OPENAI_MODEL="gpt-4o-mini"
```

Then run:

```bash
python main.py
```

Open `Assignment_25.ipynb` and run each task separately so the notebook contains real execution output.

## RAG

The supplied `data/knowledge.txt` is a small local knowledge base. Task 9 loads it, splits it, creates OpenAI embeddings, stores them in FAISS, retrieves relevant chunks and passes them into an LCEL generation chain.

## Important

No model responses are fabricated. If `OPENAI_API_KEY` is missing, API-dependent tasks report that the key is needed. Fill `MY_RUN_NOTES.txt` with the results from your own run.

## Folder

- `main.py`
- `Assignment_25.ipynb`
- `requirements.txt`
- `README.md`
- `MY_RUN_NOTES.txt`
- `data/knowledge.txt`
- `outputs/`
