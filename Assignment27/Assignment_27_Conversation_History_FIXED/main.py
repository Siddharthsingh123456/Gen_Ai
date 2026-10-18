import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
model = ChatOllama(model=model_name, temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use earlier messages when a question is a follow-up."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

chain = prompt | model


# Task 4: keep only recent messages
def trim_history(history, max_messages=6):
    if len(history) <= max_messages:
        return history
    return history[-max_messages:]


# Task 4: also limit history by an approximate token count.
# This is useful when the conversation is long.
def trim_history_by_tokens(history, max_tokens=700):
    kept = []
    total = 0

    for message in reversed(history):
        text = str(message.content)
        # Simple estimate: about 4 characters per token.
        estimated_tokens = max(1, len(text) // 4)

        if total + estimated_tokens > max_tokens:
            break

        kept.insert(0, message)
        total += estimated_tokens

    return kept


def ask_question(history, question):
    message_history = trim_history(history, 6)
    message_history = trim_history_by_tokens(message_history, 700)

    result = chain.invoke({
        "chat_history": message_history,
        "question": question
    })

    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=result.content))

    return history, result


def run_demo():
    history = []

    questions = [
        "Explain Python lists in simple words.",
        "Give me one example.",
        "What about tuples?"
    ]

    print("Assignment 27 - Conversation History")
    print("Model:", model_name)

    for question in questions:
        print("\nUser:", question)
        try:
            history, result = ask_question(history, question)
            print("Assistant:", result.content)
        except Exception as error:
            print("Error:", error)
            print("Check that Ollama is running and the model is installed.")

    print("\nStored messages:", len(history))
    print("After 4-message trimming:", len(trim_history(history, 4)))
    print("After token trimming:", len(trim_history_by_tokens(history, 100)))


if __name__ == "__main__":
    run_demo()
