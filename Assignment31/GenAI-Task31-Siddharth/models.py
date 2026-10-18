"""Factories for the embedding model (Task 3) and the chat LLM (no fine-tuning)."""
import os

import config


class ConfigError(Exception):
    """Missing API key / bad configuration - printed as a friendly message."""


def get_embeddings():
    """OpenAI, HuggingFace (free, local) or Ollama embeddings - chosen in .env."""
    provider = config.EMBEDDING_PROVIDER
    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=config.HF_EMBEDDING_MODEL)
    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=config.OLLAMA_EMBEDDING_MODEL)
    if not os.getenv("OPENAI_API_KEY"):
        raise ConfigError("OPENAI_API_KEY is missing. Add it to .env, or set "
                          "EMBEDDING_PROVIDER=huggingface for free local embeddings.")
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL)


def get_llm():
    """OpenAI, Groq (free tier) or Ollama (local) chat model - chosen in .env."""
    provider = config.LLM_PROVIDER
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=config.OLLAMA_MODEL, temperature=0)
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            raise ConfigError("GROQ_API_KEY is missing. Add it to .env.")
        from langchain_groq import ChatGroq
        return ChatGroq(model=config.GROQ_MODEL, temperature=0)
    if not os.getenv("OPENAI_API_KEY"):
        raise ConfigError("OPENAI_API_KEY is missing. Add it to .env, or set "
                          "LLM_PROVIDER=groq / ollama for a free option.")
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=config.OPENAI_CHAT_MODEL, temperature=0)
