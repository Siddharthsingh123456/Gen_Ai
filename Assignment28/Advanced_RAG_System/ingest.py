"""PART 1 & 2 - Document ingestion, chunking, embeddings, vector store, retriever.

Run `python ingest.py` to execute Tasks 1-4 and print the required outputs.
"""
import argparse
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


# ----------------------------------------------------------------- Task 1
def load_documents(data_dir: Path = config.DATA_DIR) -> List[Document]:
    """Load every .txt and .pdf file inside `data_dir` using LangChain loaders."""
    docs: List[Document] = []
    for path in sorted(Path(data_dir).glob("*")):
        if path.suffix.lower() == ".txt":
            docs.extend(TextLoader(str(path), encoding="utf-8").load())
        elif path.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(path)).load())
    if not docs:
        raise FileNotFoundError(f"No .txt or .pdf files found in {data_dir}")
    return docs


# ----------------------------------------------------------------- Task 2
def split_documents(docs: List[Document]) -> List[Document]:
    """Split documents into overlapping chunks with RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    return splitter.split_documents(docs)


# ----------------------------------------------------------------- Task 3 & 4
def build_vector_store(chunks: List[Document], embeddings, persist: bool = True) -> FAISS:
    """Embed the chunks and store them in a FAISS index (saved to disk)."""
    store = FAISS.from_documents(chunks, embeddings)
    if persist:
        config.VECTOR_STORE_DIR.mkdir(exist_ok=True)
        store.save_local(str(config.VECTOR_STORE_DIR))
    return store


def load_vector_store(embeddings) -> FAISS:
    return FAISS.load_local(
        str(config.VECTOR_STORE_DIR), embeddings, allow_dangerous_deserialization=True
    )


def get_retriever(store: FAISS, k: int = config.TOP_K):
    """Create a retriever from the vector store."""
    return store.as_retriever(search_kwargs={"k": k})


def get_or_build_retriever(embeddings, rebuild: bool = False):
    """Reuse the saved index if it exists, otherwise ingest and build it."""
    index_file = config.VECTOR_STORE_DIR / "index.faiss"
    if index_file.exists() and not rebuild:
        store = load_vector_store(embeddings)
    else:
        chunks = split_documents(load_documents())
        store = build_vector_store(chunks, embeddings)
    return get_retriever(store)


# ----------------------------------------------------------------- demo
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true",
                        help="use fake embeddings (no API key / downloads)")
    args = parser.parse_args()

    docs = load_documents()
    print("=== Task 1: Load Documents ===")
    print("Number of documents :", len(docs))
    print("Sample content      :", docs[0].page_content[:300].replace("\n", " "), "...\n")

    chunks = split_documents(docs)
    print("=== Task 2: Text Splitting ===")
    print(f"chunk_size={config.CHUNK_SIZE}, chunk_overlap={config.CHUNK_OVERLAP}")
    print("Total chunks        :", len(chunks), "\n")

    if args.offline:
        from langchain_core.embeddings import DeterministicFakeEmbedding
        embeddings = DeterministicFakeEmbedding(size=256)
    else:
        from models import get_embeddings
        embeddings = get_embeddings()

    store = build_vector_store(chunks, embeddings)
    retriever = get_retriever(store)
    print("=== Task 3 & 4: Embeddings + Vector Store ===")
    print("FAISS index saved to:", config.VECTOR_STORE_DIR)
    hits = retriever.invoke("What is a vector database?")
    print("Retriever test query returned", len(hits), "chunks")
