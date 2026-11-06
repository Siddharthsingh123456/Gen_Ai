"""Central configuration for the Conversational PDF Q&A chatbot."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_PDF = DATA_DIR / "sample_handbook.pdf"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"      # one sub-folder per PDF (cached index)

# ---- Task 2: chunking ----
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ---- Task 4: retriever ----
TOP_K = 4

# ---- Task 8: history trimming ----
MAX_HISTORY_MESSAGES = 6     # keep the last 6 messages (3 user/AI turns)
MAX_HISTORY_TOKENS = 800     # approximate token budget
TRIM_MODE = "messages"       # "messages" or "tokens"

# ---- providers (set in .env) ----
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()                # openai | groq | ollama
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()    # openai | huggingface | ollama

OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
