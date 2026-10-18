"""
Assignment 25 - Prompting & LangChain Chains

This project demonstrates the 10 tasks in the assignment brief.
Set OPENAI_API_KEY before running tasks that call an OpenAI model.

Example:
    python -m pip install -r requirements.txt
    python main.py

The code does not fabricate model responses. If an API key/model is unavailable,
the program reports the actual error and still demonstrates local Pydantic/runnable
parts that do not require an API call.
"""

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

def title(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def task1_prompt_templates():
    title("TASK 1 - PROMPT TEMPLATE")

    from langchain_core.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(
        "You are a helpful assistant.\n"
        "Answer this question in simple language:\n"
        "{question}"
    )

    question = "What is LangChain?"
    print("Template variables:", prompt.input_variables)
    print("Formatted prompt:")
    print(prompt.format(question=question))

def task2_chat_prompt():
    title("TASK 2 - CHATPROMPTTEMPLATE & MESSAGETEMPLATES")

    from langchain_core.prompts import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful AI tutor. Keep answers clear and short."
        ),
        HumanMessagePromptTemplate.from_template(
            "Explain {topic} for a beginner."
        ),
    ])

    messages = chat_prompt.format_messages(topic="prompt templates")
    for message in messages:
        print(message.type + ":", message.content)

def task3_pydantic():
    title("TASK 3 - PYDANTIC OUTPUT SCHEMA")

    from pydantic import BaseModel, Field
    from langchain_core.output_parsers import PydanticOutputParser

    class Answer(BaseModel):
        answer: str
        confidence: float = Field(ge=0, le=1)
        source: str

    parser = PydanticOutputParser(pydantic_object=Answer)
    print("Schema:")
    print(parser.get_format_instructions())

    valid_data = Answer(
        answer="LangChain helps compose language-model application components.",
        confidence=0.94,
        source="knowledge.txt"
    )
    print("\nValidated object:")
    print(valid_data)

    print("\nExample invalid input:")
    try:
        Answer(answer="test", confidence=2.0, source="demo")
    except Exception as exc:
        print(type(exc).__name__ + ":", exc)

def task4_validation():
    title("TASK 4 - VALIDATION & ERROR HANDLING")

    from pydantic import BaseModel, Field, ValidationError

    class ChatAnswer(BaseModel):
        answer: str
        confidence: float = Field(ge=0, le=1)
        source: str

    examples = [
        {"answer": "valid", "confidence": 0.8, "source": "local"},
        {"answer": "bad confidence", "confidence": 1.5, "source": "local"},
    ]

    for item in examples:
        try:
            result = ChatAnswer(**item)
            print("Validated:", result)
        except ValidationError as exc:
            print("Validation failed:")
            print(exc)

def build_llm():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0
    )

def task5_simple_chain():
    title("TASK 5 - SIMPLE CHAIN")

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(
        "Explain {topic} in exactly two simple sentences."
    )
    chain = prompt | build_llm() | StrOutputParser()

    print("Chain: Prompt -> LLM -> OutputParser")
    try:
        print(chain.invoke({"topic": "LangChain chains"}))
    except Exception as exc:
        print("LLM execution error:", type(exc).__name__, exc)

def make_retriever():
    """Create a local FAISS retriever from the supplied knowledge file."""
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS

    documents = TextLoader(str(DATA / "knowledge.txt"), encoding="utf-8").load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=80
    ).split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def task6_conditional():
    title("TASK 6 - CONDITIONAL CHAIN")

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableBranch

    answer_prompt = ChatPromptTemplate.from_template(
        "Answer this factual question using concise language: {question}"
    )
    fallback_prompt = ChatPromptTemplate.from_template(
        "Say that the question needs a human review: {question}"
    )

    llm = build_llm()
    branch = RunnableBranch(
        (lambda x: "?" in x["question"], answer_prompt | llm | StrOutputParser()),
        fallback_prompt | llm | StrOutputParser()
    )

    try:
        print(branch.invoke({"question": "What is a conditional chain?"}))
    except Exception as exc:
        print("LLM execution error:", type(exc).__name__, exc)

def task7_parallel():
    title("TASK 7 - PARALLEL CHAIN")

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableParallel

    llm = build_llm()

    answer_chain = (
        ChatPromptTemplate.from_template(
            "Give one short definition of {topic}."
        ) | llm | StrOutputParser()
    )
    summary_chain = (
        ChatPromptTemplate.from_template(
            "Give one short summary of why {topic} is useful."
        ) | llm | StrOutputParser()
    )

    parallel = RunnableParallel(
        answer=answer_chain,
        summary=summary_chain
    )

    try:
        print(parallel.invoke({"topic": "LangChain"}))
    except Exception as exc:
        print("LLM execution error:", type(exc).__name__, exc)

def task8_runnables_lcel():
    title("TASK 8 - RUNNABLES & LCEL")

    from langchain_core.runnables import RunnableLambda, RunnablePassthrough

    clean = RunnableLambda(lambda x: x.strip())
    chain = RunnablePassthrough() | clean

    print("Input:", "  LangChain LCEL  ")
    print("Output:", chain.invoke("  LangChain LCEL  "))
    print("LCEL uses composable Runnable objects and the | operator.")

def task9_rag():
    title("TASK 9 - LCEL-BASED RAG CHAIN")

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    try:
        retriever = make_retriever()
        prompt = ChatPromptTemplate.from_template(
            "Use only the context below to answer the question.\n\n"
            "Context:\n{context}\n\nQuestion: {question}"
        )
        llm = build_llm()

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs,
             "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        print(rag_chain.invoke("Why is chunk overlap important?"))
    except Exception as exc:
        print("RAG execution error:", type(exc).__name__, exc)
        print("RAG requires OPENAI_API_KEY because this example uses OpenAI embeddings.")

def task10_observations():
    title("TASK 10 - OBSERVATIONS & INSIGHTS")
    print("1. Structured output makes downstream processing safer because fields are validated.")
    print("2. Chains make an application modular: prompt, model and parser can be changed separately.")
    print("3. LCEL makes multi-step workflows readable and composable.")
    print("4. Use parallel chains when outputs are independent and can be generated together.")
    print("5. Use conditional chains when different inputs need different processing paths.")
    print("6. RAG is useful when answers should be grounded in a private or changing knowledge base.")

def main():
    task1_prompt_templates()
    task2_chat_prompt()
    task3_pydantic()
    task4_validation()
    task8_runnables_lcel()

    if os.getenv("OPENAI_API_KEY"):
        task5_simple_chain()
        task6_conditional()
        task7_parallel()
        task9_rag()
    else:
        print("\nOPENAI_API_KEY is not set.")
        print("Tasks 5-7 and 9 are available but were not called, so no fake model output is shown.")

    task10_observations()

if __name__ == "__main__":
    main()
