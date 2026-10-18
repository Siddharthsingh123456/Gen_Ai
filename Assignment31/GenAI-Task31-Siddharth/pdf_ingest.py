"""PART 1 & 2 - PDF ingestion, chunking, embeddings, vector store, retriever (Tasks 1-4).

Run:  python pdf_ingest.py                      (uses data/sample_handbook.pdf)
      python pdf_ingest.py --pdf my_book.pdf
"""
import argparse
import hashlib
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


# ----------------------------------------------------------------- Task 1
def load_pdf(path) -> List[Document]:
    """Load a PDF with PyPDFLoader (one Document per page, page number in metadata)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"'{path.name}' is not a PDF file.")
    pages = PyPDFLoader(str(path)).load()
    for p in pages:
        p.metadata["source"] = path.name
    if not any(p.page_content.strip() for p in pages):
        raise ValueError("No text found in this PDF (a scanned PDF needs OCR first).")
    return pages


# ----------------------------------------------------------------- Task 2
def split_pages(pages: List[Document], chunk_size: int = config.CHUNK_SIZE,
                chunk_overlap: int = config.CHUNK_OVERLAP) -> List[Document]:
    """Split PDF pages into overlapping chunks (page metadata is kept on every chunk)."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return [c for c in splitter.split_documents(pages) if c.page_content.strip()]


# ----------------------------------------------------------------- Task 3 & 4
def build_vector_store(chunks: List[Document], embeddings, save_dir=None) -> FAISS:
    store = FAISS.from_documents(chunks, embeddings)
    if save_dir:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        store.save_local(str(save_dir))
    return store


def get_retriever(store: FAISS, k: int = config.TOP_K):
    return store.as_retriever(search_kwargs={"k": k})


def _cache_dir(data: bytes, chunk_size: int, chunk_overlap: int) -> Path:
    key = hashlib.md5(data + f"{chunk_size}-{chunk_overlap}-{config.EMBEDDING_PROVIDER}".encode()).hexdigest()[:12]
    return config.VECTOR_STORE_DIR / key


def retriever_for_pdf(path, embeddings, chunk_size: int = config.CHUNK_SIZE,
                      chunk_overlap: int = config.CHUNK_OVERLAP, k: int = config.TOP_K):
    """PDF -> chunks -> FAISS (cached on disk per PDF) -> retriever. Returns (retriever, n_pages, n_chunks)."""
    path = Path(path)
    pages = load_pdf(path)
    cache = _cache_dir(path.read_bytes(), chunk_size, chunk_overlap)
    if (cache / "index.faiss").exists():
        store = FAISS.load_local(str(cache), embeddings, allow_dangerous_deserialization=True)
        n_chunks = store.index.ntotal
    else:
        chunks = split_pages(pages, chunk_size, chunk_overlap)
        store = build_vector_store(chunks, embeddings, cache)
        n_chunks = len(chunks)
    return get_retriever(store, k), len(pages), n_chunks


# ----------------------------------------------------------------- demo (prints Task 1-4 output)
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=str(config.SAMPLE_PDF))
    ap.add_argument("--offline", action="store_true", help="fake embeddings (no key needed)")
    args = ap.parse_args()

    pages = load_pdf(args.pdf)
    print("=== Task 1: Load PDF ===")
    print("File            :", Path(args.pdf).name)
    print("Number of pages :", len(pages))
    print("Sample page (page 1, first 300 characters):")
    print("  ", pages[0].page_content[:300].replace("\n", " "), "...\n")

    chunks = split_pages(pages)
    print("=== Task 2: Text Splitting ===")
    print(f"chunk_size={config.CHUNK_SIZE}, chunk_overlap={config.CHUNK_OVERLAP}")
    print("Total chunks    :", len(chunks))
    print("Chunk 1 preview :", chunks[0].page_content[:150].replace("\n", " "), "...\n")

    if args.offline:
        from langchain_core.embeddings import DeterministicFakeEmbedding
        emb = DeterministicFakeEmbedding(size=256)
    else:
        from models import get_embeddings
        emb = get_embeddings()
    store = build_vector_store(chunks, emb)
    hits = get_retriever(store).invoke("How many days of annual leave do employees get?")
    print("=== Task 3 & 4: Embeddings + Vector Store (FAISS) ===")
    print(f"Embedded and stored {len(chunks)} chunks; retriever returned {len(hits)} chunks "
          f"(pages {sorted({h.metadata.get('page', 0) + 1 for h in hits})})")
