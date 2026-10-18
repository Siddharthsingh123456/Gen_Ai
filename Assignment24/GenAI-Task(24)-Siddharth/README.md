# Assignment 24: Ollama Chatbot

**Author:** Siddharth

A local LLM-powered chatbot built with **Ollama** and **LangChain**, with every
call traced in **LangSmith**.

## Files
| File | Purpose |
|------|---------|
| `basic_chat.py` | Task 1: single prompt to Ollama via LangChain's `ChatOllama`, prints the response |
| `chatbot.py` | Interactive multi-turn chatbot with conversation history |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for LangSmith / model configuration |

## Setup

### 1. Install and run Ollama
Download from https://ollama.com/download, then verify:
```bash
ollama --version
ollama serve        # skip if the Ollama app is already running
```

### 2. Pull a model
```bash
ollama pull llama3      # or: ollama pull mistral
```

### 3. Install Python dependencies
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure LangSmith
1. Create a free account at https://smith.langchain.com and generate an API key.
2. Copy `.env.example` to `.env` and paste your key:
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your key>
LANGSMITH_PROJECT=ollama-chatbot-assignment-24
OLLAMA_MODEL=llama3
```

## Run
```bash
python basic_chat.py    # simple prompt + response
python chatbot.py       # interactive chatbot
```

## How it works
- `ChatOllama` (from `langchain-ollama`) wraps the local Ollama server at `http://localhost:11434`.
- `chatbot.py` builds a LangChain chain: `ChatPromptTemplate | ChatOllama | StrOutputParser`,
  and passes the running message history so the bot remembers context.
- Setting `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` makes LangChain send every run
  (prompt, response, latency, token usage) to LangSmith automatically, with no extra code.

## LangSmith tracking
Open https://smith.langchain.com, then the project **ollama-chatbot-assignment-24**.
Each chatbot turn appears as a trace showing input, output, latency, and the
prompt -> model -> parser steps. The screenshot is attached with the submission.

## Troubleshooting
- `Connection refused`: Ollama isn't running; start it with `ollama serve`.
- `model not found`: run `ollama pull llama3` (or set `OLLAMA_MODEL` to a model you pulled).
- No traces in LangSmith: check the API key and that `LANGSMITH_TRACING=true` is set in `.env`.
