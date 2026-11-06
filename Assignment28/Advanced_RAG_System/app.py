"""PART 6 - Task 10 (optional): Streamlit chat UI.   Run: streamlit run app.py"""
import streamlit as st

import ingest
from models import get_embeddings, get_llm
from rag_chain import ConversationalRAG

st.set_page_config(page_title="Document Q&A (Conversational RAG)", page_icon="📚")
st.title("📚 Document Q&A Chatbot")
st.caption("LangChain RAG with message history - answers come only from your documents.")


@st.cache_resource(show_spinner="Loading documents and vector store...")
def load_retriever():
    return ingest.get_or_build_retriever(get_embeddings())


if "bot" not in st.session_state:
    st.session_state.bot = ConversationalRAG(get_llm(), load_retriever())
    st.session_state.display = []          # [(role, text)] for rendering

with st.sidebar:
    if st.button("Clear conversation"):
        st.session_state.bot.reset()
        st.session_state.display = []
        st.rerun()

for role, text in st.session_state.display:
    st.chat_message(role).write(text)

if question := st.chat_input("Ask a question about the documents..."):
    st.chat_message("user").write(question)
    with st.spinner("Thinking..."):
        answer, docs = st.session_state.bot.ask(question)
    st.chat_message("assistant").write(answer)
    with st.expander("Sources"):
        for d in docs:
            st.markdown(f"**{d.metadata.get('source', 'unknown')}**")
            st.caption(d.page_content[:300] + "...")
    st.session_state.display += [("user", question), ("assistant", answer)]
