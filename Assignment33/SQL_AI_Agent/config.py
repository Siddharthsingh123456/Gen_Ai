"""Shared configuration: DB URIs and LLM factory."""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, "company.db")
SQLITE_URI = f"sqlite:///{SQLITE_PATH}"
# Read-only connection used by the agent (agent can never modify data)
SQLITE_RO_URI = f"sqlite:///file:{SQLITE_PATH}?mode=ro&uri=true"

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "company_db")
MYSQL_SERVER_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}"
MYSQL_URI = f"{MYSQL_SERVER_URI}/{MYSQL_DB}"


def get_llm():
    """Return a chat model based on LLM_PROVIDER (openai | groq | ollama)."""
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), temperature=0)
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.1"), temperature=0)
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")
