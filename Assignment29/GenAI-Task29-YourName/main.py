import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

chat_history = []

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Q&A assistant. Give clear and simple answers."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

def get_model(model_type="openai"):
    if model_type.lower() == "ollama":
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2"))
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0
    )

def get_answer(question, model_type="openai"):
    """Task 7: one function for switching between OpenAI and Ollama."""
    model = get_model(model_type)

    messages = prompt.format_messages(
        history=chat_history,
        question=question
    )

    response = model.invoke(messages)
    answer = response.content

    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    return answer

def main():
    print("Assignment 29 - Unified Q&A Chatbot")
    print("Type 'exit' to stop.")
    model_type = input("Choose model (openai/ollama): ").strip().lower()

    if model_type not in ["openai", "ollama"]:
        print("Invalid model. Using openai.")
        model_type = "openai"

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break

        try:
            print("Assistant:", get_answer(question, model_type))
        except Exception as error:
            print("Error:", error)
            print("Check your API key or Ollama model.")

if __name__ == "__main__":
    main()
