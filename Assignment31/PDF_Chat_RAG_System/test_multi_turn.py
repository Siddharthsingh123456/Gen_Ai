"""PART 5 - Task 9: follow-up Q&A testing with the real LLM.   Run: python test_multi_turn.py

Verifies: context is preserved across turns and answers stay grounded in the PDF.
"""
import config
import pdf_ingest
from models import get_embeddings, get_llm
from rag_chain import ConversationalPDFChat, page_of

TURNS = [
    ("1. Initial factual question",     "How many days of paid annual leave do full-time employees get?"),
    ("2. Follow-up (uses prev. answer)", "How many of those days can I carry forward to next year?"),
    ("3. Clarification question",       "What happens to the remaining days after that?"),
    ("4. Follow-up: explain more",      "Explain more about the sick leave rules."),
    ("5. Not in the PDF (grounding)",   "What is the company's stock price today?"),   # expect "I don't know."
]

retriever, n_pages, n_chunks = pdf_ingest.retriever_for_pdf(config.SAMPLE_PDF, get_embeddings())
bot = ConversationalPDFChat(get_llm(), retriever)
print(f"PDF: {n_pages} pages, {n_chunks} chunks\n")

for label, question in TURNS:
    answer, docs = bot.ask(question)
    print(f"--- {label} ---")
    print("Q:", question)
    print("A:", answer)
    print("Pages used:", sorted({page_of(d) for d in docs}))
    print("History size:", len(bot.history.messages), "messages (trimmed to max", config.MAX_HISTORY_MESSAGES, ")\n")
