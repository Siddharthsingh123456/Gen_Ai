import streamlit as st
from main import get_answer, chat_history

st.set_page_config(page_title="Q&A Chatbot", page_icon="💬")
st.title("💬 Unified Q&A Chatbot")

model_type = st.selectbox(
    "Choose a model",
    ["openai", "ollama"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_answer(question, model_type)
                st.write(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as error:
                st.error(str(error))
