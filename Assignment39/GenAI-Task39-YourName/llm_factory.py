"""LLM + secret helpers. Works the same locally, on Streamlit Cloud and on Hugging Face Spaces."""
import os

PROVIDERS = {
    "Groq (free tier)": {"key_name": "GROQ_API_KEY", "default_model": "llama-3.3-70b-versatile"},
    "OpenAI": {"key_name": "OPENAI_API_KEY", "default_model": "gpt-4o-mini"},
}


def get_secret(name: str) -> str:
    """Read a secret from Streamlit secrets (Streamlit Cloud / secrets.toml) or an
    environment variable (Hugging Face Spaces secrets, local shell, .env)."""
    try:
        import streamlit as st
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:       # no secrets file configured
        pass
    return os.environ.get(name, "")


def get_llm(provider: str, model: str, temperature: float, api_key: str):
    if provider.startswith("Groq"):
        from langchain_groq import ChatGroq
        return ChatGroq(model=model, temperature=temperature, api_key=api_key)
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
