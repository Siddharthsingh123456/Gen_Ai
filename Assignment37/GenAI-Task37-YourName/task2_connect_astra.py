"""TASK 2 - Connect to AstraDB with LangChain using token + endpoint, and verify the connection."""
from rag_core import (ASTRA_ENDPOINT, ASTRA_TOKEN, COLLECTION, get_astra_database,
                      get_embeddings, get_vector_store, check_astra_env)

check_astra_env()
print("Endpoint:", ASTRA_ENDPOINT)
print("Token   :", ASTRA_TOKEN[:12] + "..." + "(hidden)")

# 1) Verify token + endpoint with the raw Data API client
db = get_astra_database()
print("\n[1] Connected to database. Existing collections:", db.list_collection_names())

# 2) Connect through the LangChain integration (creates the collection if missing)
embeddings = get_embeddings()
print("\n[2] Embedding dimension:", len(embeddings.embed_query("test")))
vstore = get_vector_store(embeddings)
print(f"    LangChain AstraDBVectorStore ready -> collection '{COLLECTION}'")

# 3) Verify: the collection now exists and answers queries
print("\n[3] Collections now:", db.list_collection_names())
print("    Test search returned", len(vstore.similarity_search("connection test", k=1)), "result(s) (0 is fine on an empty DB)")
print("\nConnection verified.")
