# Assignment 37: AstraDB RAG (PDF Query System)

A PDF question-answering system built with LangChain and a cloud vector database
(DataStax AstraDB).

**Pipeline:** `PDF -> Splitter -> Embeddings -> AstraDB -> Retriever -> LLM -> Answer`

## Project structure
| File | Task |
|------|------|
| `Readme.md` | Task 1 steps + observations & insights |
| `rag_core.py` | Shared code: AstraDB connection, embeddings, LLM, PDF loading/splitting, RAG answer function |
| `task2_connect_astra.py` | Task 2: connect with token + endpoint and verify |
| `task3_load_split_pdf.py` | Task 3: load PDF (PyPDFLoader) and split into chunks |
| `task4_store_embeddings.py` | Task 4: embed + store in AstraDB, verify persistence |
| `app.py` | Task 5: Streamlit PDF Query RAG app (session state) |
| `task6_testing.py` | Task 6: 5 PDF questions, source validation, out-of-context questions |
| `test_offline.py` | Logic test that runs without AstraDB or any model |
| `data/sample.pdf` | Sample 4-page PDF ("The Rise of Renewable Energy") |
| `.env.example` | Copy to `.env` and fill in your Astra + LLM keys |

## Task 1 – Getting started with AstraDB (manual steps in the browser)
1. **Create a DataStax Astra account:** go to https://astra.datastax.com and sign up (free tier available).
2. **Create a vector database:** *Databases -> Create Database -> Serverless (Vector)*. Choose a name,
   provider and region, keep the default keyspace (`default_keyspace`) and click *Create*.
   Wait until the status is **Active**.
3. **Generate the application token and endpoint:**
   - Token: *Database -> Overview -> Application Token -> Generate Token* (role *Database Administrator*).
     Copy the value that starts with `AstraCS:` (shown only once).
   - API Endpoint: shown on the same Overview page (`https://<db-id>-<region>.apps.astra.datastax.com`).
4. Put both into `.env`:
   ```
   ASTRA_DB_APPLICATION_TOKEN=AstraCS:...
   ASTRA_DB_API_ENDPOINT=https://....apps.astra.datastax.com
   ```
   The collection (`pdf_rag`) is created automatically by the code on first use.

## How to run
```bash
pip install -r requirements.txt
cp .env.example .env              # fill in Astra token/endpoint and an LLM key (Groq/OpenAI) or use Ollama

python task2_connect_astra.py     # Task 2: verify connection
python task3_load_split_pdf.py    # Task 3: load + split (works without any account)
python task4_store_embeddings.py  # Task 4: store embeddings, verify persistence
streamlit run app.py              # Task 5: the application (upload a PDF in the sidebar)
python task6_testing.py           # Task 6: testing and validation
```
Use your own PDF with e.g. `python task4_store_embeddings.py my.pdf`.

## How each task is implemented
- **Task 2:** `AstraDBVectorStore(token=..., api_endpoint=...)` from `langchain-astradb`.
  Verified by listing collections through the Data API client and running a test search.
- **Task 3:** `PyPDFLoader` (one Document per page) and `RecursiveCharacterTextSplitter`
  (chunk size 1000, overlap 150). Metadata keeps file name and page number.
- **Task 4:** embeddings from HuggingFace `all-MiniLM-L6-v2` (free, local) or OpenAI (set `EMBEDDING_PROVIDER`).
  Chunks get deterministic IDs, so uploading the same PDF again updates them rather than creating duplicates.
  Persistence is checked with a fresh connection that counts the stored documents and still finds chunks.
- **Task 5:** Streamlit app: upload and index a PDF, ask questions, get grounded answers with the
  source pages. The prompt tells the LLM to answer only from the retrieved context.
- **Task 6:** five PDF questions (answer must contain the expected fact *and* the retrieved chunks
  must contain it too, proving the answer comes from the document), plus two out-of-context
  questions that must return the fallback message *"I couldn't find that in the uploaded document."*

## Observations & Insights

**1. Why is AstraDB useful for production RAG?**
- It is a managed, serverless cloud vector database: no servers to run, automatic scaling and backups.
- Vectors are stored persistently, so documents are embedded once and available to every user and
  every restart of the app.
- Supports metadata filtering (file name, page, user), so one collection can serve many documents and tenants.
- Built on Apache Cassandra, giving high availability, low latency and multi-region replication.
- Simple API and a first-class LangChain integration; access is controlled by tokens/roles.

**2. Importance of session state in GenAI apps**
Streamlit reruns the whole script on every interaction. Session state keeps data between reruns:
the chat history, the list of indexed files, and expensive objects such as the AstraDB connection,
the embedding model and the LLM (created once instead of on every message). Without it, the
conversation would vanish after each question and models would reload every time. Session state is
per user session; long-term data (the vectors) lives in AstraDB.

**3. Difference between FAISS and AstraDB**

| | FAISS | AstraDB |
|---|---|---|
| Type | Open-source library for similarity search, runs in your process | Managed cloud vector database service |
| Persistence | In memory; you must save/load index files yourself | Built-in persistent storage |
| Scaling | Limited to one machine's memory/disk | Scales horizontally in the cloud |
| Multi-user / sharing | Hard: each app holds its own index | Many apps and users share the same data |
| Metadata filtering, updates, deletes | Basic and awkward | Rich filtering, easy upserts/deletes |
| Setup / cost | Free, no account, very fast and ideal for prototypes | Needs an account and a network call; free tier, then paid |
| Best for | Local experiments, small static datasets | Production RAG with shared, changing data |

## Notes
- `test_offline.py` was run successfully here (PDF splitting, deterministic IDs with no duplicates on
  re-ingest, retrieval, grounded answer and out-of-context fallback), using an in-memory store and a fake LLM.
  AstraDB itself could not be reached from my environment, so the AstraDB steps (Tasks 2, 4, 5, 6)
  need to be run on your machine with your own Astra account.
- If you change the embedding model after creating the collection, use a new `ASTRA_DB_COLLECTION`
  name, because vector dimensions (384 for MiniLM, 1536 for OpenAI small) must match.
- Take screenshots for submission: Astra dashboard showing the database and collection, the
  Streamlit app answering questions with sources, and the `task6_testing.py` output.
