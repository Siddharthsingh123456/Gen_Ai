# Assignment 22 - Embedding Models, Vector Stores & Similarity Search

## Dataset
The project uses pre-split chunks from the document-loading/splitting workflow
of Assignment 21. `data/chunks.json` contains 8 small document chunks with
source metadata. Replace these sample chunks with the actual chunks generated
from your Assignment 21 documents before final submission if required by your mentor.

## Included tasks
1. OpenAI Embedding Model
2. Hugging Face Embedding Model
3. OpenAI vs Hugging Face comparison
4. OpenAI cosine-similarity search with 3 queries
5. LangChain similarity-search abstraction
6. Ollama local embeddings
7. FAISS vector store, save and reload
8. ChromaDB persistent vector store
9. FAISS vs ChromaDB comparison
10. End-to-end pipeline
11. Observations and insights

## Installation
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## OpenAI
Set `OPENAI_API_KEY` before Tasks 1, 4, 5, 7 and 8.

Windows PowerShell:
$env:OPENAI_API_KEY="your-key"

Optional model:
$env:OPENAI_EMBEDDING_MODEL="text-embedding-3-small"

## Hugging Face
The default model is:
sentence-transformers/all-MiniLM-L6-v2

Optional:
HF_EMBEDDING_MODEL

## Ollama
Install Ollama locally, then pull an embedding model such as:
ollama pull nomic-embed-text

The default model is `nomic-embed-text`.

## Run
python main.py

Important:
The code does not fabricate API responses, embeddings, similarity scores,
FAISS results or ChromaDB results. If a service/key/model is unavailable,
that task reports the actual reason and skips the live operation.

## Vector-store explanation
FAISS is useful for fast local similarity indexing.
ChromaDB is useful when persistent collections and database-style management
are preferred.

## RAG connection
The workflow is:
Documents -> chunks -> embeddings -> vector store -> similarity search -> retrieved context -> LLM.
