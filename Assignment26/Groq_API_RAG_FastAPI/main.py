"""
Assignment 26 - Groq API Chatbot, RAG & FastAPI Serving

Run:
    python main.py

Set GROQ_API_KEY before running real Groq calls:
    PowerShell: $env:GROQ_API_KEY="your-key"

No model response is fabricated. If the key is missing, the program reports it.
"""

import os

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def create_groq_client():
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")
    return Groq(api_key=api_key)


def groq_chat(user_message: str, system_message: str = "You are a helpful assistant.") -> str:
    """Send one user message to Groq and return the model text."""
    client = create_groq_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def task1_groq_setup():
    print("\n=== TASK 1: GROQ API SETUP & BASIC CHAT ===")
    print("Model:", MODEL)
    if not os.getenv("GROQ_API_KEY"):
        print("GROQ_API_KEY is missing. Set it before making a real API call.")
        return
    try:
        print(groq_chat("Explain Groq API in two simple sentences."))
    except Exception as exc:
        print("Groq error:", type(exc).__name__, exc)


def task2_chatbot():
    print("\n=== TASK 2: GROQ CHATBOT ===")
    questions = [
        "What is FastAPI?",
        "What is RAG?",
        "Why should API keys be kept in environment variables?",
    ]

    if not os.getenv("GROQ_API_KEY"):
        print("Skipping real model calls because GROQ_API_KEY is not set.")
        return

    for question in questions:
        print("\nUser:", question)
        try:
            print("Assistant:", groq_chat(question))
        except Exception as exc:
            print("Error:", type(exc).__name__, exc)


def build_rag_chain():
    """Build a simple local FAISS + Groq RAG pipeline."""
    from langchain_community.document_loaders import TextLoader
    from langchain_community.vectorstores import FAISS
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_groq import ChatGroq
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set.")

    # Embeddings require an embedding provider. OpenAI embeddings are used here
    # only when OPENAI_API_KEY is available. This avoids pretending that Groq
    # supplies an embedding endpoint in this assignment.
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is required for this FAISS embedding demo. "
            "Alternatively replace OpenAIEmbeddings with your chosen local embedding model."
        )

    documents = TextLoader(
        "data/knowledge.txt", encoding="utf-8"
    ).load()

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=60
    ).split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        model=MODEL,
        temperature=0,
        groq_api_key=os.environ["GROQ_API_KEY"],
    )

    prompt = ChatPromptTemplate.from_template(
        """Answer the question using only the context below.
If the answer is not present in the context, say that the context does not contain it.

Context:
{context}

Question:
{question}
"""
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    return retriever, format_docs, prompt, llm, chunks


def task3_rag():
    print("\n=== TASK 3: GROQ-BASED RAG PIPELINE ===")
    try:
        retriever, format_docs, prompt, llm, chunks = build_rag_chain()
        print("Number of document chunks:", len(chunks))

        question = "Why should API keys be stored in environment variables?"
        docs = retriever.invoke(question)
        context = format_docs(docs)

        messages = prompt.invoke({"context": context, "question": question})
        answer = llm.invoke(messages)

        print("\nRetrieved context:")
        print(context)
        print("\nGroq answer:")
        print(answer.content)
    except Exception as exc:
        print("RAG setup/execution error:", type(exc).__name__, exc)


def task4_rag_prompt_template():
    print("\n=== TASK 4: PROMPT TEMPLATE FOR GROQ RAG ===")
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Answer only from the retrieved context. Do not add unsupported facts."
        ),
        (
            "human",
            "Retrieved context:\n{context}\n\nUser question:\n{question}"
        ),
    ])

    print(prompt.format(
        context="FastAPI is a Python framework for building APIs.",
        question="What is FastAPI?"
    ))


def task5_fastapi():
    print("\n=== TASK 5: FASTAPI APPLICATION ===")
    print("The FastAPI application is in app.py.")
    print("Run: uvicorn app:app --reload")
    print("Endpoint: POST /chat")


def task6_fastapi_groq():
    print("\n=== TASK 6: FASTAPI + GROQ INTEGRATION ===")
    print("app.py validates the request with Pydantic and calls groq_chat().")
    print("Use POST /chat with JSON: {\"query\": \"Your question here\"}")


def task7_run_instructions():
    print("\n=== TASK 7: RUN & TEST FASTAPI LOCALLY ===")
    print("uvicorn app:app --reload")
    print("Open http://127.0.0.1:8000/docs")
    print("Test POST /chat from Swagger UI or Postman.")


def task8_production_readiness():
    print("\n=== TASK 8: PRODUCTION READINESS ===")
    print("1. Store GROQ_API_KEY in an environment variable.")
    print("2. Do not commit .env or API keys to Git.")
    print("3. Validate request data with Pydantic.")
    print("4. Add exception handling around external API calls.")
    print("5. Configure CORS only for trusted frontend origins in production.")


def task9_demo():
    print("\n=== TASK 9: END-TO-END DEMO ===")
    questions = [
        "What is Groq?",
        "Why is FastAPI useful?",
        "What is RAG?"
    ]
    print("Prepared test questions:", len(questions))
    print("Run the FastAPI server and test each question with POST /chat.")
    print("Record the real responses in MY_RUN_NOTES.txt.")


def task10_observations():
    print("\n=== TASK 10: OBSERVATIONS & INSIGHTS ===")
    print("1. Groq is useful for low-latency model inference in API applications.")
    print("2. Groq can serve the generation part of a RAG pipeline.")
    print("3. FastAPI provides a simple HTTP interface for frontend or other clients.")
    print("4. API-first GenAI architecture separates the model service from the UI.")
    print("5. Retrieval can ground answers in a supplied document collection.")


def main():
    task1_groq_setup()
    task2_chatbot()
    task3_rag()
    task4_rag_prompt_template()
    task5_fastapi()
    task6_fastapi_groq()
    task7_run_instructions()
    task8_production_readiness()
    task9_demo()
    task10_observations()


if __name__ == "__main__":
    main()
