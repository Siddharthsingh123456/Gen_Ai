"""Factories for the embedding model (Task 3) and the chat LLM."""
import config


def get_embeddings():
    """Return an embedding model: OpenAI or HuggingFace (selected in .env)."""
    if config.EMBEDDING_PROVIDER == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=config.HF_EMBEDDING_MODEL)

    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL)


def get_llm():
    """Return a chat model: OpenAI or Ollama (selected in .env). No fine-tuning."""
    if config.LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=config.OLLAMA_MODEL, temperature=0)

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=config.OPENAI_CHAT_MODEL, temperature=0)
