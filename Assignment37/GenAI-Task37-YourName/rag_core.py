"""Shared RAG logic: AstraDB vector store, embeddings, LLM, PDF loading/splitting, answering.

Pipeline:  PDF -> Splitter -> Embeddings -> AstraDB -> Retriever -> LLM -> Answer
"""
import hashlib
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

ASTRA_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE") or None
COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "pdf_rag")

NOT_FOUND = "I couldn't find that in the uploaded document."


# ------------------------------------------------------------------ models
def get_embeddings():
    provider = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=os.getenv(
        "HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))


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


# ------------------------------------------------------------------ AstraDB
def check_astra_env():
    missing = [n for n, v in [("ASTRA_DB_APPLICATION_TOKEN", ASTRA_TOKEN),
                              ("ASTRA_DB_API_ENDPOINT", ASTRA_ENDPOINT)] if not v]
    if missing:
        raise RuntimeError(f"Missing in .env: {', '.join(missing)} (see Readme.md, Task 1)")


def get_astra_database():
    """Raw astrapy handle (used for verification: list collections, count documents)."""
    from astrapy import DataAPIClient
    check_astra_env()
    client = DataAPIClient(ASTRA_TOKEN)
    return client.get_database_by_api_endpoint(ASTRA_ENDPOINT, keyspace=ASTRA_KEYSPACE)


def get_vector_store(embeddings=None, collection_name: str = COLLECTION):
    """Connect to AstraDB with token + endpoint. The collection is created on first use."""
    from langchain_astradb import AstraDBVectorStore
    check_astra_env()
    return AstraDBVectorStore(
        collection_name=collection_name,
        embedding=embeddings or get_embeddings(),
        token=ASTRA_TOKEN,
        api_endpoint=ASTRA_ENDPOINT,
        namespace=ASTRA_KEYSPACE,
    )


# ------------------------------------------------------------------ PDF
def load_pdf(path: str):
    """Load a PDF with LangChain's PyPDFLoader (one Document per page)."""
    from langchain_community.document_loaders import PyPDFLoader
    pages = PyPDFLoader(path).load()
    name = os.path.basename(path)
    for p in pages:
        page_no = int(p.metadata.get("page", 0)) + 1              # human-friendly (1-based)
        p.metadata = {"source": name, "page": page_no}            # keep metadata small for AstraDB
    return pages


def split_documents(pages, chunk_size: int = 1000, chunk_overlap: int = 150):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(pages)


def load_and_split_pdf(path: str, chunk_size: int = 1000, chunk_overlap: int = 150):
    """Task 3: load PDF -> split into chunks ready for embedding."""
    return split_documents(load_pdf(path), chunk_size, chunk_overlap)


def make_ids(chunks):
    """Deterministic IDs: re-uploading the same PDF updates chunks instead of duplicating them."""
    ids = []
    for i, c in enumerate(chunks):
        key = f"{c.metadata.get('source')}|{c.metadata.get('page')}|{i}|{c.page_content}"
        ids.append(hashlib.sha1(key.encode("utf-8")).hexdigest())
    return ids


def ingest_pdf(path: str, vector_store, chunk_size: int = 1000, chunk_overlap: int = 150) -> int:
    """Task 4: embed chunks and store them in the vector store. Returns number of chunks."""
    chunks = load_and_split_pdf(path, chunk_size, chunk_overlap)
    vector_store.add_documents(chunks, ids=make_ids(chunks))
    return len(chunks)


# ------------------------------------------------------------------ RAG
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a document question-answering assistant. Answer ONLY from the context below, "
     "which comes from the user's PDF. Be concise and factual. "
     f"If the context does not contain the answer, reply exactly: \"{NOT_FOUND}\" "
     "Do not use outside knowledge.\n\nContext:\n{context}"),
    ("human", "{question}"),
])


def format_context(docs) -> str:
    return "\n\n".join(f"[{d.metadata.get('source')} p.{d.metadata.get('page')}] {d.page_content}"
                       for d in docs)


def answer_question(vector_store, llm, question: str, k: int = 4):
    """Task 5: retriever -> LLM -> grounded answer. Returns {'answer', 'sources'}."""
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    chain = RAG_PROMPT | llm | StrOutputParser()
    answer = chain.invoke({"context": format_context(docs), "question": question}).strip()
    sources = [{"source": d.metadata.get("source"), "page": d.metadata.get("page"),
                "text": d.page_content} for d in docs]
    if NOT_FOUND.lower().rstrip(".") in answer.lower():
        sources = []                       # no grounded answer -> no citations
    return {"answer": answer, "sources": sources}
