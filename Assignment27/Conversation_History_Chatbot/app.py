import os
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

st.title("Assignment 27 - Chatbot with Conversation History")
st.caption("Ollama + LangChain")

if "history" not in st.session_state:
    st.session_state.history = []

model = ChatOllama(model=model_name, temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use earlier messages when a question is a follow-up."),
    MessagesPlaceholder("chat_history"),
    ("human", "{question}")
])

chain = prompt | model


def trim_history(history, max_messages=6):
    if len(history) <= max_messages:
        return history
    return history[-max_messages:]


def trim_history_by_tokens(history, max_tokens=700):
    kept = []
    total = 0

    for message in reversed(history):
        estimated_tokens = max(1, len(str(message.content)) // 4)

        if total + estimated_tokens > max_tokens:
            break

        kept.insert(0, message)
        total += estimated_tokens

    return kept


for message in st.session_state.history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.write(message.content)

question = st.chat_input("Ask a question")

if question:
    with st.chat_message("user"):
        st.write(question)

    history_for_model = trim_history(st.session_state.history)
    history_for_model = trim_history_by_tokens(history_for_model)

    try:
        result = chain.invoke({
            "chat_history": history_for_model,
            "question": question
        })

        with st.chat_message("assistant"):
            st.write(result.content)

        st.session_state.history.append(HumanMessage(content=question))
        st.session_state.history.append(AIMessage(content=result.content))

    except Exception as error:
        st.error("Could not get a response from Ollama.")
        st.write(error)
