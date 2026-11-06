"""PART 5 - Task 9: multi-turn testing with real Groq.   Run: python test_multi_turn.py

Checks: initial factual question, follow-up question, out-of-context question,
and that chat history is maintained.
"""
import rag_backend as rb

TURNS = [
    ("Initial factual question", "What is an LPU and why is Groq fast?"),
    ("Follow-up question",       "Explain more about how that helps latency."),
    ("Out-of-context question",  "Who is the prime minister of Japan?"),   # expect "I don't know..."
]

docs = rb.load_sample_documents()
bot, n_chunks = rb.build_bot_from_docs(docs, rb.get_llm())
print(f"Indexed {len(docs)} documents into {n_chunks} chunks\n")

for label, question in TURNS:
    result = bot.ask(question)
    print(f"--- {label} ---")
    print("Q:", question)
    print("A:", result.answer)
    print("Sources:", sorted({d.metadata['source'] for d in result.docs}))
    print(f"Latency: {result.latency:.2f}s | history: {len(bot.history)} messages\n")

assert len(bot.history) == 6, "chat history should hold 3 turns"
print("History maintained across turns.")
