# Assignment 26 — Groq API Chatbot, RAG & FastAPI Serving

This project follows the supplied TuteDude Assignment 26 brief.

## Tasks

1. Groq API setup and basic chat
2. Groq chatbot function and multiple questions
3. Groq-based RAG pipeline
4. Prompt template for context-grounded RAG
5. FastAPI application
6. FastAPI + Groq integration with Pydantic validation
7. Local Uvicorn serving and API testing
8. Basic production-readiness practices
9. End-to-end validation plan
10. Observations and insights

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Set the Groq key:

PowerShell:

```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
$env:GROQ_MODEL="llama-3.1-8b-instant"
```

Then run:

```bash
python main.py
```

## FastAPI

Start:

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Test:

```json
{
  "query": "What is RAG?"
}
```

## RAG note

The example uses Groq for generation and FAISS for retrieval. The supplied local
`data/knowledge.txt` is split into chunks. The current example uses OpenAI
embeddings because Groq is being used as the generation API here and does not
provide the embedding endpoint assumed by this assignment.

Therefore the RAG demo needs both:

- `GROQ_API_KEY`
- `OPENAI_API_KEY`

If you want a fully local embedding model, replace `OpenAIEmbeddings` with an
embedding implementation available in your environment.

## No fake execution

The project does not invent Groq responses or claim that a deployment occurred.
Run the API yourself and record genuine outputs in `MY_RUN_NOTES.txt`.
