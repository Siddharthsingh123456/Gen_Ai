"""Offline logic test - no Groq key, no model download.  Run: python test_offline.py"""
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel

import rag_backend as rb

docs = rb.load_sample_documents()
chunks = rb.split_documents(docs)
assert len(docs) == 3 and len(chunks) > len(docs)
print(f"[ok] {len(docs)} docs -> {len(chunks)} chunks")

# uploaded-file path (bytes) incl. error handling
up = rb.load_uploaded_files([("notes.txt", b"Groq runs models on LPUs. " * 80)])
assert up[0].metadata["source"] == "notes.txt"
for bad in ([("x.docx", b"hi")], [("empty.txt", b"   ")]):
    try:
        rb.load_uploaded_files(bad)
        raise SystemExit("should have failed")
    except ValueError:
        pass
print("[ok] uploaded files loaded; unsupported / empty files rejected")

# missing key -> friendly error
import os
os.environ.pop("GROQ_API_KEY", None)
rb.config.GROQ_API_KEY = ""
try:
    rb.get_llm()
    raise SystemExit("should have failed")
except rb.ConfigError:
    print("[ok] missing GROQ_API_KEY handled")

llm = FakeListChatModel(responses=[
    "An LPU is Groq's inference chip.",                    # turn 1 answer
    "How does the LPU reduce latency?",                    # turn 2 rewrite
    "Its deterministic design removes scheduling delays.", # turn 2 answer (streamed)
    "Who is the prime minister of Japan?",                 # turn 3 rewrite
    rb.NOT_FOUND,                                          # turn 3 answer
])
bot, n = rb.build_bot_from_docs(docs, llm, DeterministicFakeEmbedding(size=128))
r1 = bot.ask("What is an LPU?")
assert r1.answer and len(r1.docs) == 4 and len(bot.history) == 2

streamed = "".join(bot.ask_stream("Explain more."))      # follow-up through the streaming path
assert streamed and len(bot.history) == 4 and bot.last_first_token > 0
r3 = bot.ask("Who is the prime minister of Japan?")
assert r3.answer == rb.NOT_FOUND and len(bot.history) == 6
print("[ok] 3 turns: answer, streamed follow-up, out-of-context ->", repr(r3.answer))

for i in range(5):
    bot._remember(f"q{i}", f"a{i}")
assert len(bot.history) <= 6 and bot.history[0].type == "human"
print("[ok] history trimmed to", len(bot.history), "messages")
print("\nAll offline checks passed.")
