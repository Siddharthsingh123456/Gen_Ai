"""Shared helpers: build HuggingFace-backed LangChain LLMs (local or via HF API)."""
import os
from dotenv import load_dotenv

load_dotenv()

HF_MODE = os.getenv("HF_MODE", "local").lower()
TEXT_MODEL = os.getenv("HF_TEXT_MODEL", "google/flan-t5-base")
CHAT_MODEL = os.getenv("HF_CHAT_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN") or None

if TOKEN:                                   # makes huggingface_hub / transformers pick it up
    os.environ["HF_TOKEN"] = TOKEN
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = TOKEN


def get_text_llm(model_id: str = TEXT_MODEL, max_new_tokens: int = 128):
    """LangChain LLM (string in -> string out) backed by an open-source seq2seq model (flan-t5)."""
    if HF_MODE == "api":
        from langchain_huggingface import HuggingFaceEndpoint
        return HuggingFaceEndpoint(repo_id=model_id, task="text2text-generation",
                                   max_new_tokens=max_new_tokens, temperature=0.1)
    from langchain_huggingface import HuggingFacePipeline
    return HuggingFacePipeline.from_model_id(
        model_id=model_id,
        task="text2text-generation",
        pipeline_kwargs={"max_new_tokens": max_new_tokens},
    )


def get_causal_llm(model_id: str = CHAT_MODEL, max_new_tokens: int = 200):
    """LangChain LLM (string in -> string out) backed by a decoder-only chat/instruct model."""
    if HF_MODE == "api":
        from langchain_huggingface import HuggingFaceEndpoint
        return HuggingFaceEndpoint(repo_id=model_id, task="text-generation",
                                   max_new_tokens=max_new_tokens, temperature=0.3)
    from langchain_huggingface import HuggingFacePipeline
    return HuggingFacePipeline.from_model_id(
        model_id=model_id,
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": max_new_tokens, "return_full_text": False,
                         "do_sample": False},
    )


def get_chat_model(llm=None):
    """Wrap a HuggingFace LLM in ChatHuggingFace so it accepts chat messages (system/human/ai)
    and applies the model's own chat template."""
    from langchain_huggingface import ChatHuggingFace
    return ChatHuggingFace(llm=llm or get_causal_llm())
