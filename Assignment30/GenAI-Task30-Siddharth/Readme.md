# GenAI Task 30 - Chat Groq RAG Application with Streamlit UI

**Student:** Siddharth

A fast, real-time **document Q&A chatbot**. Users upload PDF / text files in the browser,
the app indexes them on the fly (RAG) and answers questions using **Groq** (via **ChatGroq**)
for ultra-low-latency responses. The UI is built with **Streamlit** and keeps the conversation history.

Restrictions followed: ChatGroq + LangChain + Streamlit only, no fine-tuning.

## Features

- **Fast:** Groq inference + token streaming (`st.write_stream`); first-token and total latency shown under every answer
- **Grounded:** answers only from retrieved chunks; otherwise *"I don't know based on the provided documents."*
- **Dynamic documents:** upload PDF/TXT files, indexed per session into an in-memory FAISS store
- **Conversational:** chat history kept in `st.session_state`; follow-ups ("Explain more") are rewritten into standalone questions before retrieval; history is trimmed to the last 6 messages
- **Graceful errors:** missing API key, unsupported / empty / scanned files, rate limits and network errors show friendly messages instead of crashing
- **Sources:** each answer has an expandable list of the chunks it used
- Switch Groq model (Llama 3.3 70B / Llama 3.1 8B) and tune `chunk_size`, `chunk_overlap`, `k` from the sidebar

## Project structure

```
GenAI-Task30-Siddharth/
├── Readme.md
├── requirements.txt
├── .env.example            <- copy to .env and add GROQ_API_KEY
├── config.py               <- model names, chunk size/overlap, top-k, history limit
├── groq_basic_chat.py      <- PART 1: Tasks 1-2 (ChatGroq setup + basic chat + latency)
├── rag_backend.py          <- PART 2 & 3: Tasks 3-6 (load/split, embeddings, FAISS, prompt, chain)
├── app.py                  <- PART 4 & 6: Tasks 7, 8, 10 (Streamlit UI + RAG integration)
├── test_multi_turn.py      <- PART 5: Task 9 (multi-turn test with real Groq)
├── test_offline.py         <- logic tests with fake models (no key needed)
└── data/                   <- 3 sample text files (~1100 words) for testing
```

## Task-to-file mapping

| Task | What | Where |
|------|------|-------|
| 1 | Groq account/API key, env variable, initialise ChatGroq | `rag_backend.get_llm()`, `.env` |
| 2 | Basic prompt, print response, verify low latency | `groq_basic_chat.py` |
| 3 | Load PDF/TXT with LangChain loaders; RecursiveCharacterTextSplitter (`chunk_size`, `chunk_overlap`) | `rag_backend.load_file()`, `split_documents()` |
| 4 | Embeddings (HuggingFace / OpenAI / Ollama) + FAISS + retriever | `rag_backend.get_embeddings()`, `build_vector_store()`, `get_retriever()` |
| 5 | ChatPromptTemplate: injects context, takes question, "answer only from context" | `rag_backend.QA_PROMPT` |
| 6 | Chain: Question -> Retriever -> Context -> Prompt -> ChatGroq -> Answer | `rag_backend.build_rag_chain()`, `GroqRAG` |
| 7 | Streamlit: file uploader, chat input, chat messages, session state | `app.py` |
| 8 | On query: retrieve -> generate with ChatGroq -> show in chat format | `app.py` + `GroqRAG.ask_stream()` |
| 9 | Multi-turn testing | `test_multi_turn.py` |
| 10 | Final app: dynamic loading, fast, history, error handling | `app.py` |
| 11 | Observations | section below |

## Architecture

```
Upload PDF/TXT ─► loaders ─► RecursiveCharacterTextSplitter ─► embeddings ─► FAISS ─► retriever
                                                                                        │
user question ─► (rewrite with chat history) ───────────────────────────────────────────┤
                                                                                        ▼
           QA prompt: system(rules + context) + MessagesPlaceholder(history) + question ─► ChatGroq ─► streamed answer
```

Groq has no embedding API, so embeddings come from another provider. The default is a free
local HuggingFace model (`all-MiniLM-L6-v2`); OpenAI or Ollama embeddings can be selected in `.env`.

## Setup

```bash
python -m venv venv
venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt

copy .env.example .env           # macOS/Linux: cp .env.example .env
# open .env and paste your key:  GROQ_API_KEY=gsk_...      (free key: https://console.groq.com/keys)
```

## Run

```bash
python groq_basic_chat.py          # Tasks 1-2: basic Groq chat + latency
python test_multi_turn.py          # Task 9: multi-turn RAG test
streamlit run app.py               # Tasks 7, 8, 10: the full app
python test_offline.py             # logic tests without any API key
```

In the app: upload your PDF/TXT files -> **Process uploaded documents** -> ask questions.
(Or click **Use sample documents** to try it instantly with the files in `data/`.)

Test checklist (Task 9): initial factual question -> follow-up ("Explain more...") ->
out-of-context question (should answer "I don't know...") -> chat history stays on screen.

## Task 11 - Observations & Insights

**1. Why Groq is suitable for RAG chatbots**
A RAG request already has extra steps (retrieval, a longer prompt full of context, sometimes a
question-rewrite call), so the LLM call is the latency bottleneck. Groq runs open models on LPU
hardware with very low time-to-first-token and high tokens/second, so the whole pipeline feels
real-time, and streaming makes answers appear almost instantly. Large context windows (~128K) fit
retrieved chunks plus history, and the API is simple to use through LangChain's `ChatGroq`.

**2. Difference between Groq RAG and OpenAI RAG**
The RAG architecture (load -> chunk -> embed -> retrieve -> prompt -> generate) is identical; only
the generation step differs. Groq serves open-weight models (Llama etc.) on specialised hardware:
much faster and generally cheaper, but with a smaller model choice and no embedding API of its
own. OpenAI serves proprietary GPT models with a broader ecosystem (embeddings, multimodal, tools)
but typically higher latency/cost and closed models. Because LangChain uses a common chat-model
interface, switching only means changing the model class.

**3. Role of Streamlit in rapid GenAI prototyping**
Streamlit turns a Python script into an interactive web app with no frontend code. It has ready-made
widgets for exactly this use case (`file_uploader`, `chat_input`, `chat_message`, `write_stream`),
`session_state` for memory between reruns, and `cache_resource` to avoid reloading models. This lets
developers focus on the AI logic, iterate quickly and let others try the prototype in a browser.

## Notes

- API keys are read from environment variables / `.env` and never hard-coded. `.env` is not in the zip.
- Groq's model catalogue changes over time; if a model name stops working, set `GROQ_MODEL` in `.env`
  to one listed at https://console.groq.com/docs/models.
- Scanned PDFs without a text layer cannot be read (no OCR) - the app shows a clear error.
