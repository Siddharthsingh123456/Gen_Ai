"""Ollama chatbot with conversation memory, traced with LangSmith.
Run:  python chatbot.py     (type 'exit' to quit)"""
import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, concise AI assistant."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

llm = ChatOllama(model=MODEL, temperature=0.7)
chain = prompt | llm | StrOutputParser()


def main():
    history = []
    print(f"Ollama Chatbot ({MODEL}) - type 'exit' to quit\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue
        # run_name / tags make the trace easy to find in LangSmith
        answer = chain.invoke(
            {"question": question, "history": history},
            config={"run_name": "ollama-chatbot-turn", "tags": ["assignment-24", MODEL]},
        )
        print(f"Bot: {answer}\n")
        history.extend([HumanMessage(question), AIMessage(answer)])


if __name__ == "__main__":
    main()
