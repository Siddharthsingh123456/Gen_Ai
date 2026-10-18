# Assignment 23 — OpenAI & Retrieval-Augmented Generation (RAG)

## What this project implements

This project follows the 11 tasks in the TuteDude Assignment 23 brief:

1. OpenAI setup and basic prompt
2. Wikipedia retriever
3. Vector store retriever
4. Maximal Marginal Relevance (MMR) retriever
5. Multi-query retriever
6. Contextual compression retriever
7. YouTube transcript loading
8. OpenAI embeddings + FAISS for YouTube
9. YouTube RAG chatbot
10. Testing with 5 questions
11. Conceptual questions and observations

The code uses actual LangChain/OpenAI components. It does not create fake
responses, fake embeddings, fake transcripts, or fake similarity scores.

## Dataset / knowledge source

For the first retrieval section, the assignment uses Wikipedia as an external
knowledge source.

For the mini-project, the required source is a real YouTube video. Set:

Windows PowerShell:
$env:YOUTUBE_URL="https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

The transcript is loaded with LangChain's `YoutubeLoader`, then split into
chunks and embedded with OpenAI embeddings.

## Installation

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## OpenAI API key

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
```

Optional:

```powershell
$env:OPENAI_MODEL="gpt-4o-mini"
$env:OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
```

## YouTube

Set a real YouTube URL:

```powershell
$env:YOUTUBE_URL="https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

The video needs an accessible transcript. If transcript retrieval fails,
the program reports the actual exception rather than using a fabricated
transcript.

## Run the full assignment

```bash
python main.py
```

## Run the Streamlit chatbot

```bash
streamlit run app.py
```

Open the local Streamlit address shown in the terminal.

## RAG pipeline

The YouTube mini-project follows:

YouTube video
→ transcript
→ text chunks
→ OpenAI embeddings
→ FAISS vector store
→ similarity retrieval
→ retrieved transcript context
→ OpenAI chat model
→ answer

## Retrieval techniques

### Normal similarity search
Returns documents whose embeddings are most similar to the query.

### MMR
MMR balances relevance and diversity. This helps avoid returning several
nearly identical chunks.

### Multi-query retrieval
The LLM creates alternative query formulations. Retrieval is performed for
those formulations and the results are combined.

### Contextual compression
A compressor examines retrieved documents and keeps information relevant
to the current query before the context is passed to the model.

## Testing

Task 10 tests five questions against the selected YouTube video. Actual
results are saved to:

`output/TEST_RESULTS.json`

Do not fill this file with invented answers. Run the project first.

## Submission notes

`MY_RUN_NOTES.txt` contains a run-note template. Fill it with the actual
commands, errors, fixes, transcript details, retrieval observations, and
five test results from your own execution.
