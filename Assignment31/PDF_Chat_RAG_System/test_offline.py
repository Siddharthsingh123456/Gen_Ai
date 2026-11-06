"""Offline logic test - NO API key, NO model download.   Run: python test_offline.py

Real PDF loading + chunking + FAISS retrieval, with a fake embedding model and a scripted fake LLM.
"""
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage

import config
import pdf_ingest
from history import trim_history
from rag_chain import ConversationalPDFChat, page_of

pages = pdf_ingest.load_pdf(config.SAMPLE_PDF)
chunks = pdf_ingest.split_pages(pages)
assert len(pages) >= 4 and len(chunks) > len(pages) and "page" in chunks[0].metadata
print(f"[ok] PDF: {len(pages)} pages -> {len(chunks)} chunks (page metadata kept)")

for bad in ("missing.pdf", config.BASE_DIR / "config.py"):
    try:
        pdf_ingest.load_pdf(bad); raise SystemExit("should fail")
    except (FileNotFoundError, ValueError):
        pass
print("[ok] missing / non-PDF files rejected")

store = pdf_ingest.build_vector_store(chunks, DeterministicFakeEmbedding(size=128))
retriever = pdf_ingest.get_retriever(store)
assert len(retriever.invoke("annual leave")) == 4
print("[ok] FAISS retriever returns top-4 chunks")

llm = FakeListChatModel(responses=[
    "Employees get 24 days of annual leave (page 2).",           # turn 1
    "How many annual leave days can be carried forward?",         # turn 2 rewrite
    "Up to 10 days can be carried forward.",                      # turn 2 answer
    "What happens to unused annual leave beyond 10 days?",        # turn 3 rewrite (streamed)
    "They lapse on 31 March.",                                    # turn 3 answer
])
bot = ConversationalPDFChat(llm, retriever)
bot.ask("How many days of annual leave?")
assert len(bot.history.messages) == 2
bot.ask("How many can I carry forward?")
assert len(bot.history.messages) == 4 and page_of(bot.last_docs[0]) >= 1
tokens = list(bot.ask_stream("And the rest?"))
assert "".join(tokens) and len(bot.history.messages) == 6
print("[ok] history stored after every turn (ask + streaming):", len(bot.history.messages), "messages")

for i in range(10):
    bot.history.add_interaction(f"q{i}", f"a{i}")
kept = bot.history.messages
assert len(kept) <= config.MAX_HISTORY_MESSAGES and isinstance(kept[0], HumanMessage) and kept[-1].content == "a9"
print("[ok] message-count trimming drops oldest, keeps newest")

long = []
for i in range(30):
    long += [HumanMessage(content="question " * 60), AIMessage(content="answer " * 60)]
tok = trim_history(long, mode="tokens")
assert 0 < len(tok) < len(long) and isinstance(tok[0], HumanMessage)
print("[ok] token-length trimming works")
print("\nAll offline checks passed.")
