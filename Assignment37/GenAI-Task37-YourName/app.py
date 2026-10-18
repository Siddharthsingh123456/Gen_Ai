"""TASK 5 - PDF Query RAG application (Streamlit + LangChain + AstraDB).   Run: streamlit run app.py

Flow: PDF -> Splitter -> Embeddings -> AstraDB -> Retriever -> LLM -> Answer
"""
import os
import tempfile
import streamlit as st
from rag_core import (COLLECTION, answer_question, get_embeddings, get_llm,
                      get_vector_store, ingest_pdf)

st.set_page_config(page_title="PDF RAG with AstraDB", page_icon="📄")
st.title("📄 Chat with your PDF  (AstraDB RAG)")

# ---------------- session state ----------------
ss = st.session_state
ss.setdefault("messages", [])          # chat history shown in the UI
ss.setdefault("ingested", {})          # {file name: number of chunks stored}
ss.setdefault("vstore", None)          # AstraDB connection, created once per session
ss.setdefault("llm", None)

if ss.vstore is None:
    try:
        with st.spinner("Connecting to AstraDB and loading models..."):
            ss.vstore = get_vector_store(get_embeddings())
            ss.llm = get_llm()
    except Exception as exc:
        st.error(f"Setup problem: {exc}")
        st.stop()

# ---------------- sidebar: upload ----------------
with st.sidebar:
    st.header("1. Upload a PDF")
    uploaded = st.file_uploader("PDF file", type="pdf")
    if uploaded and uploaded.name not in ss.ingested:
        if st.button("Index PDF in AstraDB"):
            with st.spinner("Splitting, embedding and storing..."):
                with tempfile.TemporaryDirectory() as tmp:
                    path = os.path.join(tmp, uploaded.name)
                    with open(path, "wb") as f:
                        f.write(uploaded.getbuffer())
                    ss.ingested[uploaded.name] = ingest_pdf(path, ss.vstore)
            st.success(f"Indexed {ss.ingested[uploaded.name]} chunks")
    st.header("Indexed in this session")
    for name, n in ss.ingested.items():
        st.write(f"- {name} ({n} chunks)")
    st.caption(f"Collection: {COLLECTION} (data persists in AstraDB across sessions)")
    k = st.slider("Chunks to retrieve (k)", 2, 8, 4)
    if st.button("Clear chat"):
        ss.messages = []
        st.rerun()

# ---------------- chat ----------------
def show_sources(sources):
    if sources:
        with st.expander(f"Sources ({len(sources)} chunks)"):
            for s in sources:
                st.markdown(f"**{s['source']} - page {s['page']}**")
                st.caption(s["text"][:400] + ("..." if len(s["text"]) > 400 else ""))

for m in ss.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        show_sources(m.get("sources"))

question = st.chat_input("Ask a question about your PDF...")
if question:
    ss.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and answering..."):
            try:
                result = answer_question(ss.vstore, ss.llm, question, k=k)
            except Exception as exc:
                result = {"answer": f"Something went wrong: {exc}", "sources": []}
        st.markdown(result["answer"])
        show_sources(result["sources"])
    ss.messages.append({"role": "assistant", **result})
