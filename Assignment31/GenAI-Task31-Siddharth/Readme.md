# GenAI Task 31 - Conversational PDF Q&A Chatbot with Message History

**Student:** Siddharth

A chatbot that answers questions about **PDF documents** using **Retrieval-Augmented Generation (RAG)**
with **LangChain**. It remembers the conversation, understands follow-up questions
("explain more", "what about the previous topic?") and never makes up answers - if the PDF does
not contain the answer it says **"I don't know."** No fine-tuning is used.

## Project structure

```
GenAI-Task31-Siddharth/
├── Readme.md
├── requirements.txt
├── .env.example            <- copy to .env, add your key / choose provider
├── config.py               <- chunk size, overlap, top-k, history limits, providers
├── models.py               <- embedding model + chat LLM (OpenAI / Groq / Ollama / HuggingFace)
├── pdf_ingest.py           <- PART 1 & 2  (Tasks 1-4)
├── prompts.py              <- PART 3      (Task 5)
├── history.py              <- PART 4      (Tasks 7-8)
├── rag_chain.py            <- PART 4      (Task 6)
├── test_multi_turn.py      <- PART 5      (Task 9)
├── chatbot.py              <- PART 6      (Task 10, command line)
├── app.py                  <- PART 6      (Task 10, optional Streamlit UI)
├── test_offline.py         <- logic tests that need no API key
├── make_sample_pdf.py      <- script that generated the sample PDF (optional)
└── data/sample_handbook.pdf  <- 5-page sample PDF (fictional company handbook)
```

## Task-to-file mapping

| Task | What | Where |
|------|------|-------|
| 1 | Load PDF with PyPDFLoader; print number of pages + sample page content | `pdf_ingest.load_pdf()` (run `python pdf_ingest.py`) |
| 2 | RecursiveCharacterTextSplitter (`chunk_size=500`, `chunk_overlap=100`) | `pdf_ingest.split_pages()` |
| 3 | Embeddings (OpenAI / HuggingFace / Ollama) | `models.get_embeddings()` |
| 4 | FAISS vector store + retriever (top-4) | `pdf_ingest.build_vector_store()`, `get_retriever()` |
| 5 | ChatPromptTemplate: system (PDF only) + `MessagesPlaceholder` + human question; "I don't know." rule | `prompts.QA_PROMPT` |
| 6 | Chain: Question -> Retriever -> PDF Context -> Prompt + History -> LLM -> Answer | `rag_chain.build_rag_chain()` |
| 7 | Store user + AI messages after every turn; inject with `MessagesPlaceholder` | `history.ChatHistory`, `rag_chain.ConversationalPDFChat` |
| 8 | Trim history by number of messages OR token length (oldest removed) | `history.trim_history()` (`TRIM_MODE` in `config.py`) |
| 9 | Follow-up Q&A testing | `test_multi_turn.py` |
| 10 | Final chatbot (+ Streamlit UI) | `chatbot.py`, `app.py` |
| 11 | Observations | section below |

## How it works

```
PDF ─► PyPDFLoader (1 Document / page) ─► RecursiveCharacterTextSplitter ─► embeddings ─► FAISS ─► retriever

user question ─► rewrite as standalone question using history ─► retriever ─► PDF context
                                                                               │
        prompt = system(rules + context) + MessagesPlaceholder(history) + question ─► LLM ─► answer
                                                                               │
                         user + AI message stored, then oldest messages trimmed ◄┘
```

- **Follow-ups:** a question like "explain more" has no topic, so the retriever would fail. The chain first rewrites it into a standalone question using the history, then retrieves.
- **Grounding:** the system prompt restricts the model to the retrieved PDF context and tells it to say "I don't know." otherwise.
- **Page numbers:** page metadata is kept on every chunk, so answers can point to the pages they came from.
- **Memory:** after each turn the history is trimmed (default: last 6 messages = 3 turns). Switch to token-based trimming with `TRIM_MODE = "tokens"` in `config.py`.

## Setup

```bash
python -m venv venv
venv\Scripts\activate           # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt

copy .env.example .env          # macOS/Linux: cp .env.example .env
```

Then edit `.env` and choose ONE option:

| Option | .env settings |
|--------|---------------|
| OpenAI | `LLM_PROVIDER=openai`, `EMBEDDING_PROVIDER=openai`, `OPENAI_API_KEY=...` |
| Free (Groq + local embeddings) | `LLM_PROVIDER=groq`, `GROQ_API_KEY=...`, `EMBEDDING_PROVIDER=huggingface` |
| Fully local (Ollama) | `LLM_PROVIDER=ollama`, `EMBEDDING_PROVIDER=ollama` (then `ollama pull llama3.2` and `ollama pull nomic-embed-text`) |

## Run

```bash
python pdf_ingest.py             # Tasks 1-4: pages, sample content, chunks, FAISS + retriever test
python test_multi_turn.py        # Task 9: factual -> follow-up -> clarification -> not-in-PDF question
python chatbot.py                # Task 10: command-line chat  (--pdf my.pdf  --show-sources)
streamlit run app.py             # Task 10: chat UI with PDF upload
python test_offline.py           # logic tests without any key
```

Use your own PDF: `python chatbot.py --pdf path/to/book.pdf`, or upload it in the Streamlit app.

Example conversation (sample handbook):

```
You: How many days of paid annual leave do full-time employees get?
Bot: Full-time employees get 24 days of paid annual leave per calendar year (page 2).
You: How many of those can I carry forward?
Bot: Up to 10 unused days can be carried forward; the rest lapse on 31 March.
You: What is the company's stock price today?
Bot: I don't know.
```

## Task 11 - Observations & Insights

**1. Difference between PDF Q&A and conversational PDF Q&A**
Plain PDF Q&A treats each question on its own: question -> retrieve -> answer. Conversational PDF Q&A
also keeps the chat history, so references such as "those days", "that policy" or "explain more" can
be resolved. The history is used twice: to rewrite the follow-up into a complete search query for the
retriever, and (via `MessagesPlaceholder`) so the model understands the dialogue when answering.

**2. Role of message history in follow-up questions**
Follow-up questions are usually incomplete on their own. "How many can I carry forward?" has no subject,
so without history the retriever gets a vague query and returns irrelevant chunks, and the LLM cannot tell
what "many" refers to. History supplies the missing subject, keeps the context preserved across turns and
makes the chat feel natural, while the facts themselves still come from the PDF.

**3. Trade-offs between long memory and performance**
More history means better continuity, but every stored message is re-sent to the LLM on each turn. This
raises token cost and latency, can hit the context limit, and old or irrelevant messages can distract the
model and compete with the retrieved PDF chunks for space. A short window is faster and cheaper but forgets
earlier topics. This project keeps the last 6 messages as a balance, and the limit is configurable.

**4. How trimming history affects answer quality**
Trimming removes the oldest messages. Recent follow-ups keep working well, but a question that depends on
something said long ago can no longer be resolved, so the bot may retrieve the wrong passage or answer
"I don't know." Grounding is not harmed, because answers always come from the retrieved PDF text and not from
memory - only conversational continuity is lost. Trimming whole turns (always starting on a human message)
avoids half-cut, confusing history.

## Notes

- API keys come from `.env` (not included in the zip); nothing is hard-coded.
- Scanned PDFs without a text layer have no extractable text (no OCR) and give a clear error.
- The FAISS index is cached in `vector_store/` per PDF, so a PDF is embedded only once.
