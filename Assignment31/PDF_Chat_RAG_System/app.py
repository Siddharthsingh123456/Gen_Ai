"""PART 6 - Task 10 (optional): Streamlit chat UI for the PDF chatbot.   Run: streamlit run app.py"""
import tempfile
from pathlib import Path

import streamlit as st

import config
import pdf_ingest
from models import ConfigError, get_embeddings, get_llm
from rag_chain import ConversationalPDFChat, page_of

st.set_page_config(page_title="Conversational PDF Q&A", page_icon="📄", layout="wide")
st.title("📄 Conversational PDF Q&A")
st.caption("Upload a PDF and chat with it. The bot remembers the conversation and answers only from the PDF.")

for key, default in {"bot": None, "messages": [], "pdf_info": None}.items():
    st.session_state.setdefault(key, default)


@st.cache_resource(show_spinner="Loading embedding model...")
def cached_embeddings():
    return get_embeddings()


def load_pdf_into_bot(path: str, label: str):
    try:
        retriever, n_pages, n_chunks = pdf_ingest.retriever_for_pdf(path, cached_embeddings())
        bot = ConversationalPDFChat(get_llm(), retriever)
    except ConfigError as e:
        st.sidebar.error(str(e))
        return
    except Exception as e:
        st.sidebar.error(f"Could not process the PDF: {e}")
        return
    st.session_state.bot = bot
    st.session_state.messages = []
    st.session_state.pdf_info = f"{label}: {n_pages} pages, {n_chunks} chunks"


with st.sidebar:
    st.header("PDF")
    upload = st.file_uploader("Upload a PDF", type=["pdf"])
    if st.button("Process uploaded PDF", type="primary", disabled=upload is None):
        with st.spinner("Reading and indexing the PDF..."):
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / upload.name
                path.write_bytes(upload.getvalue())
                load_pdf_into_bot(str(path), upload.name)
    if st.button("Use sample PDF (company handbook)"):
        with st.spinner("Indexing the sample PDF..."):
            load_pdf_into_bot(str(config.SAMPLE_PDF), config.SAMPLE_PDF.name)
    if st.session_state.pdf_info:
        st.success(st.session_state.pdf_info)
        st.caption(f"Memory: last {config.MAX_HISTORY_MESSAGES} messages are kept.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        if st.session_state.bot:
            st.session_state.bot.reset()
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("pages"):
            st.caption("📑 Pages used: " + ", ".join(map(str, msg["pages"])))

if st.session_state.bot is None:
    st.info("👈 Upload a PDF (or click **Use sample PDF**) to start chatting.")

if question := st.chat_input("Ask a question about the PDF...", disabled=st.session_state.bot is None):
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").markdown(question)
    bot = st.session_state.bot
    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(bot.ask_stream(question))
        except Exception as e:
            answer = None
            st.error(f"Sorry, something went wrong while answering: {e}")
        if answer is not None:
            pages = sorted({page_of(d) for d in bot.last_docs})
            st.caption("📑 Pages used: " + ", ".join(map(str, pages)))
            with st.expander("Retrieved passages"):
                for d in bot.last_docs:
                    st.markdown(f"**page {page_of(d)}**")
                    st.caption(d.page_content[:300] + "...")
            st.session_state.messages.append({"role": "assistant", "content": answer, "pages": pages})
