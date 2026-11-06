"""PART 6 - Task 10: command-line chatbot.   Run: python chatbot.py"""
import argparse

import ingest
from models import get_embeddings, get_llm
from rag_chain import ConversationalRAG


def main():
    parser = argparse.ArgumentParser(description="Conversational RAG chatbot")
    parser.add_argument("--rebuild", action="store_true", help="re-ingest documents")
    parser.add_argument("--show-sources", action="store_true")
    args = parser.parse_args()

    retriever = ingest.get_or_build_retriever(get_embeddings(), rebuild=args.rebuild)
    bot = ConversationalRAG(get_llm(), retriever)

    print("Document Q&A chatbot ready. Type 'exit' to quit, 'reset' to clear memory.\n")
    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        if question.lower() == "reset":
            bot.reset()
            print("Bot: (conversation memory cleared)\n")
            continue
        answer, docs = bot.ask(question)
        print(f"Bot: {answer}\n")
        if args.show_sources:
            for d in docs:
                print("   source:", d.metadata.get("source"))
            print()


if __name__ == "__main__":
    main()
