"""TASK 4 - Embed the PDF chunks and store them in AstraDB, then verify persistence."""
import sys
from rag_core import (COLLECTION, get_astra_database, get_embeddings, get_vector_store, ingest_pdf)

path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.pdf"
embeddings = get_embeddings()                                  # 1. embedding model (HuggingFace / OpenAI)

vstore = get_vector_store(embeddings)
n = ingest_pdf(path, vstore)                                   # 2. store in the AstraDB vector store
print(f"Stored {n} chunks from '{path}' in collection '{COLLECTION}'")

# 3. Verify persistence: a brand-new connection (nothing cached in memory) must still find the data
count = get_astra_database().get_collection(COLLECTION).count_documents({}, upper_bound=100000)
print("Documents in AstraDB collection:", count)

fresh_store = get_vector_store(get_embeddings())
hits = fresh_store.similarity_search("solar panel prices", k=2)
print(f"\nFresh connection search -> {len(hits)} hit(s)")
for h in hits:
    print(f" - p.{h.metadata.get('page')}: {h.page_content[:120]}...")
print("\nData persistence verified." if hits else "\nNo hits - check the ingestion step.")
