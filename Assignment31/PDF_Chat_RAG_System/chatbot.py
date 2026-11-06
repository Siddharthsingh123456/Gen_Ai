"""PART 6 - Task 10: command-line PDF chatbot.

Run:  python chatbot.py                       (sample handbook PDF)
      python chatbot.py --pdf my_report.pdf --show-sources
"""
import argparse

import config
import pdf_ingest
from models import ConfigError, get_embeddings, get_llm
from rag_chain import ConversationalPDFChat, page_of


def main():
    ap = argparse.ArgumentParser(description="Conversational PDF Q&A chatbot")
    ap.add_argument("--pdf", default=str(config.SAMPLE_PDF), help="path to a PDF file")
    ap.add_argument("--show-sources", action="store_true", help="print the pages used")
    args = ap.parse_args()

    try:
        retriever, n_pages, n_chunks = pdf_ingest.retriever_for_pdf(args.pdf, get_embeddings())
        bot = ConversationalPDFChat(get_llm(), retriever)
    except (ConfigError, FileNotFoundError, ValueError) as e:
        raise SystemExit(f"Error: {e}")

    print(f"Loaded '{args.pdf}': {n_pages} pages, {n_chunks} chunks.")
    print("Ask questions about the PDF. Commands: 'reset' clears memory, 'exit' quits.\n")
    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        if question.lower() == "reset":
            bot.reset()
            print("Bot: (memory cleared)\n")
            continue
        try:
            answer, docs = bot.ask(question)
        except Exception as e:                        # rate limit, network, ...
            print(f"Bot: Sorry, something went wrong: {e}\n")
            continue
        print(f"Bot: {answer}\n")
        if args.show_sources:
            print("   pages used:", sorted({page_of(d) for d in docs}), "\n")


if __name__ == "__main__":
    main()
