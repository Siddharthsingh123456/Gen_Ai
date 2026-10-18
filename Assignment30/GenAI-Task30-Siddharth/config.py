"""Central configuration for the ChatGroq RAG application."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DATA_DIR = BASE_DIR / "data"

# ---- Task 1: Groq ----
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]   # shown in the UI

# ---- Task 3: chunking ----
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ---- Task 4: embeddings / retriever ----
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
TOP_K = 4

# ---- conversation memory ----
MAX_HISTORY_MESSAGES = 6      # last 3 user/AI turns are remembered
