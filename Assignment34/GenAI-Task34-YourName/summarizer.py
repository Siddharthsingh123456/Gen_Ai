"""Shared helpers: LLM factory, document loading, prompts and the four summarization strategies."""
import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# load_summarize_chain lives in `langchain.chains` (v0.x) or `langchain_classic.chains` (v1.x)
try:
    from langchain.chains.summarize import load_summarize_chain
except ImportError:  # LangChain 1.x
    from langchain_classic.chains.summarize import load_summarize_chain

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(BASE_DIR, os.getenv("DOC_PATH", "data/article.txt"))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")


# ----------------------------------------------------------------- LLM
def get_llm():
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


def _approx_tokens(llm):
    """map_reduce/refine count tokens before each call. Providers such as Groq/Ollama have no
    built-in tokenizer (LangChain would demand `transformers`), so use a ~4 chars/token estimate."""
    try:
        object.__setattr__(llm, "get_num_tokens", lambda t: max(1, len(t) // 4))
    except Exception:
        pass
    return llm


# ----------------------------------------------------------------- Loading
def load_text(path: str = DOC_PATH) -> str:
    """Load a .txt or .pdf file (via LangChain loaders) and return the full text."""
    if path.lower().endswith(".pdf"):
        from langchain_community.document_loaders import PyPDFLoader
        pages = PyPDFLoader(path).load()
        return "\n".join(p.page_content for p in pages)
    from langchain_community.document_loaders import TextLoader
    return "\n".join(d.page_content for d in TextLoader(path, encoding="utf-8").load())


def split_text(text: str, chunk_size: int = 2000, chunk_overlap: int = 200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents([text])


# ----------------------------------------------------------------- Prompts
SYSTEM_ROLE = "You are an expert summarizer who writes accurate, clear and faithful summaries."

SHORT_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nWrite a short summary (5-6 lines) of the following text.\n\n"
    "TEXT:\n{text}\n\nSHORT SUMMARY:"
)
BULLET_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nSummarize the following text as concise bullet points "
    "(one idea per bullet, max 8 bullets).\n\nTEXT:\n{text}\n\nBULLET SUMMARY:"
)

# Prompts for map_reduce / refine chains
MAP_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nSummarize this section in 2-3 sentences, keeping key facts:\n\n"
    "{text}\n\nSECTION SUMMARY:"
)
COMBINE_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nBelow are summaries of consecutive sections of one document. "
    "Combine them into one coherent final summary (about 8-10 lines), "
    "removing repetition and keeping the logical flow.\n\n{text}\n\nFINAL SUMMARY:"
)
REFINE_QUESTION_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nWrite a concise summary of the following text:\n\n{text}\n\nSUMMARY:"
)
REFINE_PROMPT = PromptTemplate.from_template(
    SYSTEM_ROLE + "\n\nExisting summary so far:\n{existing_answer}\n\n"
    "Here is more of the document:\n------------\n{text}\n------------\n"
    "Refine the existing summary using the new context. Keep it concise (8-10 lines). "
    "If the new text adds nothing, return the existing summary unchanged.\n\nREFINED SUMMARY:"
)


# ----------------------------------------------------------------- Strategies
def prompt_summary(llm, text: str, prompt: PromptTemplate = SHORT_PROMPT) -> str:
    """Part 1: plain PromptTemplate | LLM | parser (LCEL)."""
    return (prompt | llm | StrOutputParser()).invoke({"text": text})


def stuff_summary(llm, docs, custom=False) -> str:
    """Part 2: whole document stuffed into ONE prompt via load_summarize_chain."""
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.invoke({"input_documents": docs})["output_text"]


def map_reduce_summary(llm, docs, return_steps=False):
    """Part 3: summarize each chunk (map), then combine the summaries (reduce)."""
    llm = _approx_tokens(llm)
    chain = load_summarize_chain(
        llm, chain_type="map_reduce",
        map_prompt=MAP_PROMPT, combine_prompt=COMBINE_PROMPT,
        return_intermediate_steps=return_steps,
    )
    result = chain.invoke({"input_documents": docs})
    if return_steps:
        return result["output_text"], result["intermediate_steps"]
    return result["output_text"]


def refine_summary(llm, docs, return_steps=False):
    """Part 4: summarize chunk 1, then iteratively refine with each next chunk."""
    llm = _approx_tokens(llm)
    chain = load_summarize_chain(
        llm, chain_type="refine",
        question_prompt=REFINE_QUESTION_PROMPT, refine_prompt=REFINE_PROMPT,
        return_intermediate_steps=return_steps,
    )
    result = chain.invoke({"input_documents": docs})
    if return_steps:
        return result["output_text"], result["intermediate_steps"]
    return result["output_text"]


def timed(fn, *args, **kwargs):
    start = time.time()
    out = fn(*args, **kwargs)
    return out, round(time.time() - start, 2)


def save_output(name: str, content: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[saved] {path}")
