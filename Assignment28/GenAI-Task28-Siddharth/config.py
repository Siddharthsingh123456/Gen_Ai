"""Central configuration for the Conversational RAG assistant."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# ---- Task 2: chunking ----
CHUNK_SIZE = 500        # max characters per chunk
CHUNK_OVERLAP = 100     # characters shared between neighbouring chunks

# ---- Task 4: retriever ----
TOP_K = 4               # number of chunks returned per question

# ---- Task 8: history trimming ----
MAX_HISTORY_MESSAGES = 6    # keep the last 6 messages (3 user/AI turns)
MAX_HISTORY_TOKENS = 800    # approximate token budget for history
TRIM_MODE = "messages"      # "messages" or "tokens"

# ---- Model providers ----
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()                 # openai | ollama
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()     # openai | huggingface
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
