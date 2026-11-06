# GenAI Task 28 - Q&A RAG Chatbot with Message History (LangChain)

**Student:** Siddharth

A conversational Document Q&A assistant. It answers questions from text/PDF files
using **Retrieval-Augmented Generation (RAG)**, remembers previous messages, understands
follow-up questions ("Explain more", "What about the previous point?") and refuses to
hallucinate - if the answer is not in the documents it says **"I don't know."**

No fine-tuning is used. Only LangChain + an off-the-shelf LLM.

## Project structure

```
GenAI-Task28-Siddharth/
├── Readme.md             <- this file (setup + Task 11 answers)
├── requirements.txt
├── .env.example          <- copy to .env and add your key / choose provider
├── config.py             <- chunk size, overlap, top-k, history limits, providers
├── models.py             <- embedding model + chat LLM factories
├── ingest.py             <- PART 1 & 2  (Tasks 1-4)
├── prompts.py            <- PART 3      (Task 5)
├── history.py            <- PART 4      (Tasks 7-8)
├── rag_chain.py          <- PART 4      (Task 6)
├── test_multi_turn.py    <- PART 5      (Task 9)
├── chatbot.py            <- PART 6      (Task 10, command line)
├── app.py                <- PART 6      (Task 10, optional Streamlit UI)
├── test_offline.py       <- logic tests, no API key needed
└── data/                 <- 3 text files (~1200 words) used as the knowledge base
```

## Task-to-file mapping

| Task | What | Where |
|------|------|-------|
| 1 | Load documents (TextLoader / PyPDFLoader), print count + sample | `ingest.py -> load_documents()` |
| 2 | RecursiveCharacterTextSplitter (`chunk_size=500`, `chunk_overlap=100`) | `ingest.py -> split_documents()` |
| 3 | Embeddings (OpenAI or HuggingFace) | `models.py -> get_embeddings()` |
| 4 | FAISS vector store + retriever (top-k = 4) | `ingest.py -> build_vector_store(), get_retriever()` |
| 5 | ChatPromptTemplate: system + `MessagesPlaceholder` + human | `prompts.py -> QA_PROMPT` |
| 6 | Chain: Question -> Retriever -> Context -> Prompt -> LLM -> Answer | `rag_chain.py -> build_rag_chain()` |
| 7 | Store user + AI messages after every turn, pass via `MessagesPlaceholder` | `history.py -> ChatHistory`, `rag_chain.py -> ConversationalRAG` |
| 8 | Trim history by message count or tokens (oldest removed) | `history.py -> trim_history()` |
| 9 | Multi-turn testing | `test_multi_turn.py` |
| 10 | Final chatbot (+ Streamlit UI) | `chatbot.py`, `app.py` |
| 11 | Observations | section below |

## How it works

```
 user question ──► rewrite with history ──► retriever (FAISS, top-4) ──► context
        │            (standalone question)                                  │
        └──────────────► QA prompt = system(rules + context)                ▼
                                    + MessagesPlaceholder(chat_history) ──► LLM ──► answer
                                    + human(question)
```

1. **Ingestion:** files in `data/` are loaded, split into overlapping chunks, embedded and stored in FAISS (saved in `vector_store/`).
2. **Follow-up handling:** if chat history exists, the LLM first rewrites the question into a standalone one (e.g. "Explain more" -> "Explain more about the retrieval step in RAG") so the retriever searches for the right topic.
3. **Grounded answer:** the system prompt tells the model to answer only from the retrieved context, otherwise reply "I don't know."
4. **Memory:** after each turn the user and AI messages are stored, then trimmed (last 6 messages by default).

## Setup

```bash
# 1. create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate          # Windows      (macOS/Linux: source venv/bin/activate)

# 2. install
pip install -r requirements.txt

# 3. configure a provider
copy .env.example .env         # macOS/Linux: cp .env.example .env
#   Option A: OpenAI  -> put OPENAI_API_KEY in .env
#   Option B: free    -> set LLM_PROVIDER=ollama, EMBEDDING_PROVIDER=huggingface
#                        (install Ollama and run:  ollama pull llama3.2)
```

## Run

```bash
python ingest.py              # Tasks 1-4: prints doc count, sample, chunk count, builds FAISS index
python test_multi_turn.py     # Task 9: initial question -> follow-up -> clarification -> out-of-scope
python chatbot.py             # Task 10: interactive CLI  (add --show-sources to see sources)
streamlit run app.py          # Task 10: optional chat UI
python test_offline.py        # logic tests with fake models (no API key needed)
```

Use your own documents by putting `.pdf` / `.txt` files in `data/` and running `python chatbot.py --rebuild`.

Example conversation:

```
You: What is Retrieval-Augmented Generation?
Bot: RAG combines an LLM with an external knowledge source: relevant passages are retrieved and used as context ...
You: Explain more about the retrieval step.
Bot: The retriever compares the question embedding with all chunk embeddings and returns the top-k most similar chunks ...
You: Who won the 2018 FIFA World Cup?
Bot: I don't know.
```

## Task 11 - Observations & Insights

**1. Difference between normal RAG and conversational RAG**
Normal RAG treats every question independently: question -> retrieve -> answer. Conversational RAG also keeps the chat history, so it can resolve references like "it", "that point" or "explain more". It rewrites the follow-up into a standalone question for retrieval and passes the history to the prompt, so both the search and the answer are context-aware.

**2. Role of message history in follow-up questions**
A follow-up such as "Explain more" has no subject. Without history, the retriever would embed a meaningless query and return irrelevant chunks, and the LLM would not know what to expand on. History (via `MessagesPlaceholder`) supplies the missing subject, keeps the conversation coherent, and lets the model avoid repeating itself.

**3. Trade-offs between long memory and performance**
Longer memory gives better continuity but every stored message is sent to the LLM on each turn. That increases token cost, latency and the risk of hitting the context limit, and old irrelevant messages can distract the model or crowd out the retrieved context. A short window is cheaper and faster but forgets earlier topics. A balance (here: last 6 messages) is chosen.

**4. How trimming affects answer quality**
Trimming removes the oldest messages, so recent follow-ups still work well, but questions that refer to something said long ago can no longer be resolved and the bot may answer "I don't know" or retrieve the wrong topic. Because the facts always come from the retrieved documents and not from memory, answer *grounding* stays intact - only conversational continuity is lost. Trimming on whole turns (starting from a human message) avoids broken, half-cut conversations.

## Notes / design decisions

- **Hallucination control:** strict system prompt + "I don't know." fallback.
- **Vector store:** FAISS (local, no server needed).
- **Providers:** OpenAI *or* free local (HuggingFace + Ollama) - switch in `.env`; no code change.
- The `.env` file (API keys) is intentionally not included in the zip.
