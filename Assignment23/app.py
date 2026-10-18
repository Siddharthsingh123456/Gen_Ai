import os

import streamlit as st
from dotenv import load_dotenv

from main import (
    OPENAI_MODEL,
    task_7_load_youtube_transcript,
    split_youtube_documents,
    task_8_youtube_vector_store,
    make_rag_chain,
)

load_dotenv()

st.set_page_config(
    page_title="YouTube RAG Assistant",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube RAG Assistant")
st.write("Load a YouTube transcript, create embeddings, retrieve relevant chunks, and ask questions.")

if not os.getenv("OPENAI_API_KEY"):
    st.warning("OPENAI_API_KEY is not set. Add it before running the chatbot.")
    st.stop()

youtube_url = st.text_input(
    "YouTube URL",
    value=os.getenv("YOUTUBE_URL", ""),
    placeholder="https://www.youtube.com/watch?v=..."
)

if "rag_function" not in st.session_state:
    st.session_state.rag_function = None

if st.button("Load Video and Build RAG"):
    if not youtube_url:
        st.error("Enter a YouTube URL.")
    else:
        with st.spinner("Loading transcript and building vector store..."):
            try:
                documents = task_7_load_youtube_transcript(youtube_url)
                chunks = split_youtube_documents(documents)
                store = task_8_youtube_vector_store(chunks)

                # The chatbot model is created only after the data is loaded.
                from langchain_openai import ChatOpenAI
                model = ChatOpenAI(model=OPENAI_MODEL, temperature=0)

                st.session_state.rag_function = make_rag_chain(store, model)

                if st.session_state.rag_function:
                    st.success("RAG chatbot is ready.")
                else:
                    st.error("Could not build the RAG pipeline.")

            except Exception as error:
                st.error(f"Error: {error}")

if st.session_state.rag_function:
    question = st.text_input("Ask a question about the video")

    if st.button("Ask"):
        if question:
            with st.spinner("Retrieving relevant transcript chunks..."):
                answer, documents = st.session_state.rag_function(question)

            st.subheader("Answer")
            st.write(answer)

            with st.expander("Retrieved transcript chunks"):
                for number, document in enumerate(documents, start=1):
                    st.markdown(f"**Chunk {number}**")
                    st.write(document.page_content)
                    st.caption(str(document.metadata))
        else:
            st.info("Enter a question first.")
