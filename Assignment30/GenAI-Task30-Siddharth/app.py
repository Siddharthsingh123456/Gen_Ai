"""PART 4 & 6 - Streamlit UI for the ChatGroq RAG app (Tasks 7, 8, 10).

Run:  streamlit run app.py
"""
import streamlit as st

import config
import rag_backend as rb

st.set_page_config(page_title="Chat Groq RAG", page_icon="⚡", layout="wide")
st.title("⚡ Chat Groq RAG")
st.caption("Upload PDF / text documents and chat with them - powered by Groq's ultra-fast inference.")

# ------------------------------------------------ Task 7: session state
defaults = {
    "messages": [],       # chat shown on screen: dicts(role, content, sources, meta)
    "bot": None,          # GroqRAG (holds the chat history for the LLM)
    "retriever": None,
    "model": None,
    "doc_info": None,     # (n_files, n_chunks)
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)


@st.cache_resource(show_spinner="Loading embedding model (first time only)...")
def cached_embeddings():
    return rb.get_embeddings()


def index_documents(docs, model, chunk_size, chunk_overlap, k, n_files):
    """Documents -> chunks -> embeddings -> FAISS -> retriever -> bot."""
    try:
        llm = rb.get_llm(model)
        chunks = rb.split_documents(docs, chunk_size, chunk_overlap)
        store = rb.build_vector_store(chunks, cached_embeddings())
        retriever = rb.get_retriever(store, k)
    except rb.ConfigError as e:
        st.sidebar.error(str(e))
        return
    except Exception as e:                      # bad file, missing package, network ...
        st.sidebar.error(f"Could not process the documents: {e}")
        return
    st.session_state.retriever = retriever
    st.session_state.bot = rb.GroqRAG(llm, retriever)
    st.session_state.model = model
    st.session_state.doc_info = (n_files, len(chunks))
    st.session_state.messages = []
    st.sidebar.success(f"Indexed {n_files} file(s) into {len(chunks)} chunks.")


# ------------------------------------------------ sidebar
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Groq model", config.GROQ_MODELS,
                         index=config.GROQ_MODELS.index(config.GROQ_MODEL)
                         if config.GROQ_MODEL in config.GROQ_MODELS else 0)
    chunk_size = st.slider("chunk_size", 200, 1500, config.CHUNK_SIZE, 50)
    chunk_overlap = st.slider("chunk_overlap", 0, 300, config.CHUNK_OVERLAP, 10)
    top_k = st.slider("Chunks retrieved (k)", 1, 8, config.TOP_K)

    st.header("Documents")
    uploads = st.file_uploader("Upload PDF or TXT files", type=["pdf", "txt"],
                               accept_multiple_files=True)
    if st.button("Process uploaded documents", type="primary", disabled=not uploads):
        with st.spinner("Reading and indexing documents..."):
            try:
                docs = rb.load_uploaded_files([(f.name, f.getvalue()) for f in uploads])
            except Exception as e:
                st.error(f"Could not read the files: {e}")
            else:
                index_documents(docs, model, chunk_size, chunk_overlap, top_k, len(uploads))

    if st.button("Use sample documents"):
        with st.spinner("Indexing sample documents..."):
            docs = rb.load_sample_documents()
            index_documents(docs, model, chunk_size, chunk_overlap, top_k,
                            len({d.metadata["source"] for d in docs}))

    if st.session_state.doc_info:
        files, chunks = st.session_state.doc_info
        st.info(f"Ready: {files} file(s), {chunks} chunks")

    if st.button("Clear chat"):
        st.session_state.messages = []
        if st.session_state.bot:
            st.session_state.bot.reset()
        st.rerun()

# Switching model keeps the index and the conversation
if st.session_state.bot and st.session_state.model != model:
    try:
        new_bot = rb.GroqRAG(rb.get_llm(model), st.session_state.retriever)
        new_bot.history = st.session_state.bot.history
        st.session_state.bot, st.session_state.model = new_bot, model
    except rb.ConfigError as e:
        st.sidebar.error(str(e))

# ------------------------------------------------ show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            st.caption(msg["meta"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for name, preview in msg["sources"]:
                    st.markdown(f"**{name}**")
                    st.caption(preview)

# ------------------------------------------------ Task 8: chat input -> RAG -> answer
if st.session_state.bot is None:
    st.info("👈 Upload documents (or click **Use sample documents**) to start chatting.")
    if not config.GROQ_API_KEY:
        st.warning("GROQ_API_KEY not found. Add it to a `.env` file (see `.env.example`).")

question = st.chat_input("Ask a question about your documents...",
                         disabled=st.session_state.bot is None)
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    bot = st.session_state.bot
    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(bot.ask_stream(question))      # tokens appear instantly
        except Exception as e:                                       # rate limit, network, bad key ...
            answer = None
            st.error(f"Sorry, something went wrong while answering: {e}")

        if answer is not None:
            meta = (f"⚡ first token {bot.last_first_token:.2f}s · total {bot.last_latency:.2f}s "
                    f"· {st.session_state.model}")
            sources = [(d.metadata.get("source", "unknown"), d.page_content[:300] + "...")
                       for d in bot.last_docs]
            st.caption(meta)
            with st.expander("Sources"):
                for name, preview in sources:
                    st.markdown(f"**{name}**")
                    st.caption(preview)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources, "meta": meta}
            )
