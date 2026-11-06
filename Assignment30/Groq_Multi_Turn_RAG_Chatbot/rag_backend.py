"""PART 1-3 backend: Groq LLM, document loading/splitting, embeddings, vector store,
prompt template and the conversational RAG chain (Tasks 1, 3, 4, 5, 6).
"""
import os
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, trim_messages
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config

NOT_FOUND = "I don't know based on the provided documents."


class ConfigError(Exception):
    """Raised for missing keys / bad configuration (shown nicely in the UI)."""


# =========================================================== Task 1: ChatGroq
def get_llm(model: Optional[str] = None, temperature: float = 0.0):
    """Create a ChatGroq model. The API key is read from the GROQ_API_KEY env variable."""
    api_key = os.getenv("GROQ_API_KEY") or config.GROQ_API_KEY
    if not api_key:
        raise ConfigError(
            "GROQ_API_KEY is not set. Create a free key at https://console.groq.com/keys "
            "and add it to your .env file."
        )
    from langchain_groq import ChatGroq

    return ChatGroq(
        model=model or config.GROQ_MODEL,
        temperature=temperature,
        api_key=api_key,
        max_retries=2,
    )


# ============================================== Task 3: load + split documents
SUPPORTED_TYPES = {".pdf", ".txt"}


def load_file(path: str, display_name: Optional[str] = None) -> List[Document]:
    """Load one PDF/TXT file with a LangChain loader."""
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        docs = PyPDFLoader(path).load()
    elif suffix == ".txt":
        docs = TextLoader(path, encoding="utf-8", autodetect_encoding=True).load()
    else:
        raise ValueError(f"Unsupported file type '{suffix}'. Upload PDF or TXT files.")
    for d in docs:
        d.metadata["source"] = display_name or Path(path).name
    return docs


def load_uploaded_files(files: Iterable[Tuple[str, bytes]]) -> List[Document]:
    """Load files that were uploaded in the UI as (filename, bytes) pairs."""
    docs: List[Document] = []
    for name, data in files:
        suffix = Path(name).suffix.lower()
        if suffix not in SUPPORTED_TYPES:
            raise ValueError(f"'{name}' is not supported. Upload PDF or TXT files.")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            docs.extend(load_file(tmp_path, display_name=name))
        finally:
            os.unlink(tmp_path)
    if not any(d.page_content.strip() for d in docs):
        raise ValueError("No readable text found (scanned PDFs without OCR have no text).")
    return docs


def load_sample_documents() -> List[Document]:
    docs: List[Document] = []
    for p in sorted(config.SAMPLE_DATA_DIR.glob("*.txt")):
        docs.extend(load_file(str(p)))
    return docs


def split_documents(docs: List[Document], chunk_size: int = config.CHUNK_SIZE,
                    chunk_overlap: int = config.CHUNK_OVERLAP) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return [c for c in splitter.split_documents(docs) if c.page_content.strip()]


# ============================================ Task 4: embeddings + vector store
def get_embeddings():
    """HuggingFace (default, free), OpenAI or Ollama embeddings - chosen via .env."""
    provider = config.EMBEDDING_PROVIDER
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=config.OPENAI_EMBEDDING_MODEL)
    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(model=config.OLLAMA_EMBEDDING_MODEL)
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=config.HF_EMBEDDING_MODEL)


def build_vector_store(chunks: List[Document], embeddings) -> FAISS:
    """In-memory FAISS index (built fresh for the documents uploaded in this session)."""
    if not chunks:
        raise ValueError("There are no text chunks to index.")
    return FAISS.from_documents(chunks, embeddings)


def get_retriever(store: FAISS, k: int = config.TOP_K):
    return store.as_retriever(search_kwargs={"k": k})


# ================================================== Task 5: prompt templates
QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a fast, helpful document Q&A assistant.\n"
            "Answer ONLY from the retrieved context below. Never use outside knowledge.\n"
            f"If the context does not contain the answer, reply exactly: \"{NOT_FOUND}\"\n"
            "Use the chat history only to understand follow-up questions.\n"
            "Keep answers clear and concise.\n\n"
            "Retrieved context:\n{context}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user question, rewrite the question as a "
            "standalone question that makes sense without the history. Do NOT answer it. "
            "If it is already standalone, return it unchanged.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in docs)


# ======================================================= Task 6: RAG pipeline
def _prepare_chain(llm, retriever):
    """User Question -> (rewrite) -> Retriever -> Context.  Returns a runnable that adds
    'standalone', 'docs' and 'context' to the input dict."""
    parser = StrOutputParser()
    rewrite = REWRITE_PROMPT | llm | parser

    def standalone(inputs: dict) -> str:
        if not inputs["chat_history"]:          # first turn: no extra LLM call -> faster
            return inputs["question"]
        return rewrite.invoke(inputs)

    return (
        RunnablePassthrough.assign(standalone=RunnableLambda(standalone))
        | RunnablePassthrough.assign(docs=RunnableLambda(lambda x: retriever.invoke(x["standalone"])))
        | RunnablePassthrough.assign(context=RunnableLambda(lambda x: format_docs(x["docs"])))
    )


def build_rag_chain(llm, retriever):
    """Full chain: Question -> Retriever -> Context -> Prompt -> ChatGroq -> Answer."""
    return _prepare_chain(llm, retriever) | RunnablePassthrough.assign(
        answer=QA_PROMPT | llm | StrOutputParser()
    )


# ============================================== conversation + timing wrapper
@dataclass
class RAGResult:
    answer: str
    docs: List[Document]
    latency: float


class GroqRAG:
    """Keeps chat history, runs the chain, measures latency, supports token streaming."""

    def __init__(self, llm, retriever, max_history: int = config.MAX_HISTORY_MESSAGES):
        self.llm = llm
        self.prep = _prepare_chain(llm, retriever)
        self.answer_chain = QA_PROMPT | llm | StrOutputParser()
        self.max_history = max_history
        self.history: List[BaseMessage] = []
        self.last_docs: List[Document] = []
        self.last_latency: float = 0.0
        self.last_first_token: float = 0.0

    # -- memory (trim oldest messages once the limit is exceeded)
    def _remember(self, question: str, answer: str) -> None:
        self.history += [HumanMessage(content=question), AIMessage(content=answer)]
        self.history = trim_messages(
            self.history, max_tokens=self.max_history, token_counter=len,
            strategy="last", start_on="human", include_system=False,
        )

    def reset(self) -> None:
        self.history = []

    # -- normal call
    def ask(self, question: str) -> RAGResult:
        start = time.perf_counter()
        inputs = self.prep.invoke({"question": question, "chat_history": self.history})
        answer = self.answer_chain.invoke(inputs)
        self.last_latency = time.perf_counter() - start
        self.last_docs = inputs["docs"]
        self._remember(question, answer)
        return RAGResult(answer, self.last_docs, self.last_latency)

    # -- streaming call (used by the Streamlit UI for instant-feeling answers)
    def ask_stream(self, question: str) -> Iterator[str]:
        start = time.perf_counter()
        inputs = self.prep.invoke({"question": question, "chat_history": self.history})
        self.last_docs = inputs["docs"]
        parts: List[str] = []
        first = True
        for token in self.answer_chain.stream(inputs):
            if first:
                self.last_first_token = time.perf_counter() - start
                first = False
            parts.append(token)
            yield token
        self.last_latency = time.perf_counter() - start
        self._remember(question, "".join(parts))


def build_bot_from_docs(docs: List[Document], llm, embeddings=None,
                        chunk_size: int = config.CHUNK_SIZE,
                        chunk_overlap: int = config.CHUNK_OVERLAP,
                        k: int = config.TOP_K) -> Tuple[GroqRAG, int]:
    """Docs -> chunks -> embeddings -> FAISS -> retriever -> GroqRAG.  Returns (bot, n_chunks)."""
    chunks = split_documents(docs, chunk_size, chunk_overlap)
    store = build_vector_store(chunks, embeddings or get_embeddings())
    return GroqRAG(llm, get_retriever(store, k)), len(chunks)
