"""
Assignment 22: Embedding Models, Vector Stores & Similarity Search

This project uses real OpenAI, Hugging Face, Ollama, FAISS and ChromaDB
integrations. No fake embeddings or mock vector stores are used.

API/service credentials are read from environment variables.
"""

import json
import os
import time
from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).parent
CHUNKS_FILE = BASE_DIR / "data" / "chunks.json"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# ---------- PART 1: EMBEDDING MODELS ----------

def task_1_openai_embeddings(chunks):
    print("\nTASK 1 - OpenAI Embedding Model")
    try:
        from openai import OpenAI
    except ImportError:
        print("Install: pip install openai")
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Skipping live OpenAI call.")
        return None

    client = OpenAI(api_key=api_key)
    model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    start = time.perf_counter()
    response = client.embeddings.create(
        model=model_name,
        input=[item["text"] for item in chunks]
    )
    elapsed = time.perf_counter() - start

    embeddings = np.array([item.embedding for item in response.data], dtype=np.float32)

    print("Model:", model_name)
    print("Number of chunks:", len(chunks))
    print("Vector dimensions:", embeddings.shape[1])
    print("Embedding generation time: %.3f seconds" % elapsed)
    print("Sample embedding values:", embeddings[0][:10])

    return embeddings


def task_2_huggingface_embeddings(chunks):
    print("\nTASK 2 - Hugging Face Embedding Model")
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Install: pip install sentence-transformers")
        return None

    model_name = os.getenv(
        "HF_EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    start = time.perf_counter()
    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        [item["text"] for item in chunks],
        convert_to_numpy=True,
        normalize_embeddings=False,
        show_progress_bar=False
    )
    elapsed = time.perf_counter() - start

    print("Model:", model_name)
    print("Number of chunks:", len(chunks))
    print("Vector dimensions:", embeddings.shape[1])
    print("Embedding generation time: %.3f seconds" % elapsed)
    print("Sample embedding values:", embeddings[0][:10])

    return embeddings.astype(np.float32)


def task_3_model_comparison():
    print("\nTASK 3 - OpenAI vs Hugging Face")
    print("OpenAI is useful when a hosted API and strong general-purpose embeddings are preferred.")
    print("Hugging Face is useful when a local/open-source model is preferred and API cost is a concern.")
    print("Hugging Face models can be convenient for local experiments.")
    print("OpenAI requires an API key and network access; local Hugging Face inference requires model files and local compute.")


# ---------- PART 2: SIMILARITY SEARCH ----------

def cosine_similarity(query_vector, document_vectors):
    query = query_vector / (np.linalg.norm(query_vector) + 1e-12)
    docs = document_vectors / (
        np.linalg.norm(document_vectors, axis=1, keepdims=True) + 1e-12
    )
    return docs @ query


def task_4_openai_search(chunks, embeddings, queries):
    print("\nTASK 4 - Similarity Search (OpenAI Embeddings)")
    if embeddings is None:
        print("OpenAI embeddings are unavailable. Run Task 1 first with OPENAI_API_KEY.")
        return

    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    for query in queries[:3]:
        response = client.embeddings.create(model=model_name, input=query)
        query_vector = np.array(response.data[0].embedding, dtype=np.float32)
        scores = cosine_similarity(query_vector, embeddings)
        top_indices = np.argsort(scores)[::-1][:3]

        print("\nQuery:", query)
        for index in top_indices:
            print("Score: %.4f | %s" % (scores[index], chunks[index]["text"]))


def task_5_langchain_similarity_search(chunks):
    print("\nTASK 5 - LangChain Similarity Search")
    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document
        from langchain_community.vectorstores import FAISS
    except ImportError:
        print("Install: pip install langchain-openai langchain-community faiss-cpu")
        return None

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. Skipping live LangChain search.")
        return None

    documents = [
        Document(page_content=item["text"], metadata={"source": item["source"], "id": item["id"]})
        for item in chunks
    ]
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    vector_store = FAISS.from_documents(documents, embeddings)

    query = "How are documents divided into smaller retrieval pieces?"
    results = vector_store.similarity_search_with_score(query, k=3)

    print("Query:", query)
    for document, score in results:
        print("Score: %.4f | %s | %s" % (score, document.metadata, document.page_content))

    return vector_store


# ---------- PART 3: OLLAMA ----------

def task_6_ollama_embeddings(chunks):
    print("\nTASK 6 - Ollama Embedding Model")
    try:
        from langchain_ollama import OllamaEmbeddings
    except ImportError:
        print("Install: pip install langchain-ollama")
        return None

    model_name = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    print("Model:", model_name)
    print("Ollama must be installed locally and the selected model must be available.")
    print("Example preparation: ollama pull nomic-embed-text")

    try:
        embedder = OllamaEmbeddings(model=model_name)
        vectors = embedder.embed_documents([item["text"] for item in chunks])
        vectors = np.array(vectors, dtype=np.float32)
        print("Number of vectors:", len(vectors))
        print("Vector dimensions:", vectors.shape[1])
        print("Sample values:", vectors[0][:10])
        return vectors
    except Exception as error:
        print("Ollama connection/model error:", error)
        return None


# ---------- PART 4: VECTOR STORES ----------

def task_7_faiss_vector_store():
    print("\nTASK 7 - FAISS Vector Store")
    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document
        from langchain_community.vectorstores import FAISS
    except ImportError:
        print("Install: pip install langchain-openai langchain-community faiss-cpu")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. FAISS live demo skipped.")
        return

    chunks = load_chunks()
    documents = [
        Document(page_content=item["text"], metadata={"source": item["source"], "id": item["id"]})
        for item in chunks
    ]
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    store = FAISS.from_documents(documents, embeddings)

    results = store.similarity_search("What is chunk overlap?", k=2)
    print("Initial search:")
    for result in results:
        print(result.metadata, result.page_content)

    save_path = BASE_DIR / "output" / "faiss_index"
    store.save_local(str(save_path))
    print("FAISS index saved to:", save_path)

    loaded_store = FAISS.load_local(
        str(save_path),
        embeddings,
        allow_dangerous_deserialization=True
    )
    loaded_results = loaded_store.similarity_search("What is chunk overlap?", k=2)
    print("Reloaded search:")
    for result in loaded_results:
        print(result.metadata, result.page_content)


def task_8_chromadb():
    print("\nTASK 8 - ChromaDB Vector Store")
    try:
        import chromadb
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document
    except ImportError:
        print("Install: pip install chromadb langchain-chroma langchain-openai")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. ChromaDB live demo skipped.")
        return

    chunks = load_chunks()
    documents = [
        Document(page_content=item["text"], metadata={"source": item["source"], "id": item["id"]})
        for item in chunks
    ]
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    persist_directory = str(BASE_DIR / "output" / "chroma_db")
    store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="assignment22_chunks",
        persist_directory=persist_directory
    )

    results = store.similarity_search("Which component stores document vectors?", k=3)
    print("Results:")
    for result in results:
        print(result.metadata, result.page_content)

    print("Persistent Chroma directory:", persist_directory)


def task_9_faiss_vs_chroma():
    print("\nTASK 9 - FAISS vs ChromaDB")
    print("FAISS is mainly a fast similarity-search library and is convenient for local vector indexes.")
    print("ChromaDB provides a database-style vector store with collections and persistent storage.")
    print("FAISS is a strong choice for lightweight local retrieval.")
    print("ChromaDB is useful when persistence, collections and database-style management are important.")


# ---------- PART 5: MINI PROJECT ----------

def task_10_end_to_end():
    print("\nTASK 10 - End-to-End Similarity Search Pipeline")
    print("Pipeline: Documents -> Chunks -> Embeddings -> Vector Store -> Similarity Search")
    print("The implementation uses the same chunks.json data produced from the Assignment 21 workflow.")
    print("The embedding backend can be switched by choosing OpenAI, Hugging Face or Ollama.")
    print("The vector-store backend can be switched between FAISS and ChromaDB.")


def task_11_observations():
    print("\nTASK 11 - Observations & Insights")
    print("1. Embeddings convert text into numerical vectors that preserve semantic relationships.")
    print("2. Embeddings are important in GenAI because retrieval systems need to find meaningfully related content.")
    print("3. Vector databases are required when many vectors must be stored, indexed and searched efficiently.")
    print("4. This pipeline supports RAG by retrieving relevant chunks before generation.")


def main():
    print("Assignment 22 - Embedding Models, Vector Stores & Similarity Search")
    chunks = load_chunks()
    print("Loaded pre-split chunks:", len(chunks))

    openai_vectors = task_1_openai_embeddings(chunks)
    hf_vectors = task_2_huggingface_embeddings(chunks)
    task_3_model_comparison()

    queries = [
        "How does document splitting help retrieval?",
        "What does chunk overlap do?",
        "Which tools load PDF documents?"
    ]
    task_4_openai_search(chunks, openai_vectors, queries)
    task_5_langchain_similarity_search(chunks)
    task_6_ollama_embeddings(chunks)
    task_7_faiss_vector_store()
    task_8_chromadb()
    task_9_faiss_vs_chroma()
    task_10_end_to_end()
    task_11_observations()


if __name__ == "__main__":
    main()
