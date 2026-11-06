"""Offline logic test (no AstraDB / models needed): in-memory vector store + toy embeddings + fake LLM.
Run: python test_offline.py"""
import hashlib, math, re
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from rag_core import load_and_split_pdf, ingest_pdf, make_ids, answer_question, NOT_FOUND


class HashEmbeddings(Embeddings):
    """Bag-of-words hashing embeddings: deterministic and good enough to test retrieval."""
    def __init__(self, dim=256): self.dim = dim
    def _vec(self, text):
        v = [0.0] * self.dim
        for w in re.findall(r"[a-z]+", text.lower()):
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % self.dim] += 1
        n = math.sqrt(sum(x * x for x in v)) or 1
        return [x / n for x in v]
    def embed_documents(self, texts): return [self._vec(t) for t in texts]
    def embed_query(self, text): return self._vec(text)


chunks = load_and_split_pdf("data/sample.pdf")
print("chunks:", len(chunks), "| pages:", sorted({c.metadata['page'] for c in chunks}))
assert len(chunks) > 5 and len(set(make_ids(chunks))) == len(chunks)

store = InMemoryVectorStore(HashEmbeddings())
assert ingest_pdf("data/sample.pdf", store) == len(chunks)
ingest_pdf("data/sample.pdf", store)                      # same IDs -> no duplicates
assert len(store.store) == len(chunks), "re-ingest must not duplicate"

hits = store.as_retriever(search_kwargs={"k": 3}).invoke("feed-in tariff Germany market")
assert any("Germany" in h.page_content for h in hits), "retrieval should find the Germany chunk"

llm = GenericFakeChatModel(messages=iter([AIMessage(content="Germany."), AIMessage(content=NOT_FOUND)]))
r1 = answer_question(store, llm, "Which country's feed-in tariff created the market?")
assert r1["answer"] == "Germany." and r1["sources"]
r2 = answer_question(store, llm, "Who won the 2018 World Cup?")
assert r2["answer"] == NOT_FOUND and r2["sources"] == []
print("All offline logic tests passed.")
