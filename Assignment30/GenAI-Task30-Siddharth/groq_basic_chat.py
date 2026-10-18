"""PART 1 - Tasks 1 & 2: ChatGroq setup and a basic chat (no RAG).

Run:  python groq_basic_chat.py
      python groq_basic_chat.py "Explain RAG in two sentences."
"""
import sys
import time

import config
from rag_backend import get_llm


def main():
    prompt = " ".join(sys.argv[1:]) or "In two sentences, what is Retrieval-Augmented Generation?"

    llm = get_llm()                                   # Task 1: ChatGroq + API key from env

    start = time.perf_counter()
    response = llm.invoke(prompt)                     # Task 2: simple prompt
    latency = time.perf_counter() - start

    print(f"Model    : {config.GROQ_MODEL}")
    print(f"Prompt   : {prompt}")
    print(f"Response : {response.content}\n")

    # Verify low latency behaviour
    usage = response.response_metadata.get("token_usage", {})
    out_tokens = usage.get("completion_tokens")
    print(f"Latency  : {latency:.2f} s")
    if out_tokens:
        print(f"Speed    : ~{out_tokens / latency:.0f} output tokens/second ({out_tokens} tokens)")


if __name__ == "__main__":
    main()
