"""Chat model factory (OpenAI / Groq / Ollama). No fine-tuning - plain hosted/local models."""
import os

import config


class ConfigError(Exception):
    """Missing API key or bad configuration."""


def get_llm(temperature: float = 0.0):
    provider = config.LLM_PROVIDER
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=config.OLLAMA_MODEL, temperature=temperature)
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            raise ConfigError("GROQ_API_KEY is missing - add it to your .env file.")
        from langchain_groq import ChatGroq
        return ChatGroq(model=config.GROQ_MODEL, temperature=temperature)
    if not os.getenv("OPENAI_API_KEY"):
        raise ConfigError("OPENAI_API_KEY is missing - add it to .env, or set LLM_PROVIDER=groq / ollama.")
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=config.OPENAI_CHAT_MODEL, temperature=temperature)
