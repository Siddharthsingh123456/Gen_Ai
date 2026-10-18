"""
Assignment 23: OpenAI & Retrieval-Augmented Generation (RAG)

Tasks covered:
1. OpenAI setup and basic prompt
2. Wikipedia retriever
3. Vector stores retriever
4. MMR retriever
5. Multi-query retriever
6. Contextual compression retriever
7. YouTube transcript loading
8. YouTube vector store
9. YouTube RAG chatbot
10. Testing and evaluation
11. Conceptual observations

No mock OpenAI responses, fake embeddings, or fake retrieval results are used.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "")


def check_openai_key():
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        print("Set it before running the OpenAI tasks.")
        return False
    return True


# ============================================================
# PART 1 - Getting started with OpenAI
# ============================================================

def task_1_openai_basic_prompt():
    print("\n" + "=" * 70)
    print("TASK 1 - OpenAI Setup & Basic Prompt")
    print("=" * 70)

    if not check_openai_key():
        return None

    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        print("Missing package. Run: pip install langchain-openai")
        return None

    model = ChatOpenAI(model=OPENAI_MODEL, temperature=0)
    message = "Explain Retrieval-Augmented Generation in simple words."
    response = model.invoke(message)

    print("Prompt:", message)
    print("\nOpenAI response:")
    print(response.content)

    return model


# ============================================================
# PART 2 - Wikipedia + Vector Store
# ============================================================

def task_2_wikipedia_retriever():
    print("\n" + "=" * 70)
    print("TASK 2 - Wikipedia Retriever")
    print("=" * 70)

    try:
        from langchain_community.retrievers import WikipediaRetriever
    except ImportError:
        print("Missing package. Run: pip install langchain-community wikipedia")
        return []

    try:
        retriever = WikipediaRetriever(
            top_k_results=3,
            doc_content_chars_max=4000
        )

        query = "retrieval augmented generation"
        documents = retriever.invoke(query)

        print("Query:", query)
        print("Documents retrieved:", len(documents))

        for number, document in enumerate(documents, start=1):
            print(f"\nDocument {number}")
            print("Metadata:", document.metadata)
            print("Content preview:", document.page_content[:500])

        return documents

    except Exception as error:
        print("Wikipedia retrieval failed:", error)
        return []


def build_vector_store(documents):
    if not documents:
        return None

    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS
    except ImportError:
        print(
            "Missing packages. Run: "
            "pip install langchain-openai langchain-community faiss-cpu"
        )
        return None

    if not check_openai_key():
        return None

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # Add source metadata if a loader did not provide it.
    for index, document in enumerate(documents):
        document.metadata = dict(document.metadata)
        document.metadata.setdefault("document_number", index + 1)

    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store


def task_3_vector_store_retriever(wikipedia_documents):
    print("\n" + "=" * 70)
    print("TASK 3 - Vector Stores Retriever")
    print("=" * 70)

    vector_store = build_vector_store(wikipedia_documents)

    if vector_store is None:
        print("Vector store could not be created.")
        return None

    query = "What is retrieval augmented generation?"
    results = vector_store.similarity_search(query, k=3)

    print("Query:", query)
    print("Retrieved documents:", len(results))

    for number, document in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Metadata:", document.metadata)
        print("Content:", document.page_content[:700])

    return vector_store


# ============================================================
# PART 3 - Advanced Retrieval Strategies
# ============================================================

def task_4_mmr_retriever(vector_store):
    print("\n" + "=" * 70)
    print("TASK 4 - Maximal Marginal Relevance (MMR) Retriever")
    print("=" * 70)

    if vector_store is None:
        print("Vector store is unavailable.")
        return []

    normal_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    mmr_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 8, "lambda_mult": 0.5}
    )

    query = "How does RAG combine retrieval and generation?"

    normal_results = normal_retriever.invoke(query)
    mmr_results = mmr_retriever.invoke(query)

    print("Query:", query)
    print("\nNormal similarity search:")
    for number, document in enumerate(normal_results, start=1):
        print(number, document.page_content[:350])

    print("\nMMR search:")
    for number, document in enumerate(mmr_results, start=1):
        print(number, document.page_content[:350])

    print(
        "\nMMR attempts to balance relevance with diversity, "
        "so highly similar documents are less likely to dominate the results."
    )

    return mmr_results


def task_5_multi_query_retriever(vector_store, model):
    print("\n" + "=" * 70)
    print("TASK 5 - Multi-Query Retriever")
    print("=" * 70)

    if vector_store is None or model is None:
        print("Vector store or OpenAI model is unavailable.")
        return []

    try:
        from langchain_classic.retrievers import MultiQueryRetriever
    except ImportError:
        try:
            from langchain.retrievers import MultiQueryRetriever
        except ImportError:
            print(
                "MultiQueryRetriever import failed. "
                "Install/update: pip install langchain-classic"
            )
            return []

    base_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    try:
        retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=model,
            include_original=True
        )

        query = "How does RAG improve answers compared with normal prompting?"
        documents = retriever.invoke(query)

        print("Original query:", query)
        print("Documents returned:", len(documents))

        for number, document in enumerate(documents, start=1):
            print(f"\nDocument {number}")
            print(document.page_content[:600])

        return documents

    except Exception as error:
        print("Multi-query retrieval failed:", error)
        return []


def task_6_contextual_compression(vector_store, model):
    print("\n" + "=" * 70)
    print("TASK 6 - Contextual Compression Retriever")
    print("=" * 70)

    if vector_store is None or model is None:
        print("Vector store or OpenAI model is unavailable.")
        return []

    try:
        from langchain_classic.retrievers import ContextualCompressionRetriever
        from langchain_classic.retrievers.document_compressors import LLMChainExtractor
    except ImportError:
        try:
            from langchain.retrievers import ContextualCompressionRetriever
            from langchain.retrievers.document_compressors import LLMChainExtractor
        except ImportError:
            print(
                "Contextual compression imports failed. "
                "Install/update: pip install langchain-classic"
            )
            return []

    base_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    try:
        compressor = LLMChainExtractor.from_llm(model)

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

        query = "What part of RAG retrieves external information before generation?"

        before = base_retriever.invoke(query)
        after = compression_retriever.invoke(query)

        print("Query:", query)
        print("Documents before compression:", len(before))
        print("Documents after compression:", len(after))

        print("\nBefore compression:")
        for document in before:
            print(document.page_content[:450])

        print("\nAfter compression:")
        for document in after:
            print(document.page_content[:450])

        return after

    except Exception as error:
        print("Contextual compression failed:", error)
        return []


# ============================================================
# PART 4 - YouTube RAG Chatbot
# ============================================================

def task_7_load_youtube_transcript(youtube_url=None):
    print("\n" + "=" * 70)
    print("TASK 7 - Load YouTube Content")
    print("=" * 70)

    youtube_url = youtube_url or YOUTUBE_URL

    if not youtube_url:
        print("YOUTUBE_URL is not set.")
        print("Example:")
        print('Windows PowerShell: $env:YOUTUBE_URL="https://www.youtube.com/watch?v=VIDEO_ID"')
        return []

    try:
        from langchain_community.document_loaders import YoutubeLoader
    except ImportError:
        print(
            "Missing package. Run: "
            "pip install langchain-community youtube-transcript-api"
        )
        return []

    try:
        loader = YoutubeLoader.from_youtube_url(
            youtube_url,
            add_video_info=True
        )

        documents = loader.load()

        print("YouTube URL:", youtube_url)
        print("Transcript documents:", len(documents))

        for number, document in enumerate(documents[:3], start=1):
            print(f"\nDocument {number}")
            print("Metadata:", document.metadata)
            print("Transcript preview:", document.page_content[:700])

        return documents

    except Exception as error:
        print("YouTube transcript loading failed:", error)
        print(
            "Check that the video has an available transcript, "
            "the URL is correct, and internet access is working."
        )
        return []


def split_youtube_documents(documents):
    if not documents:
        return []

    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        print("Install: pip install langchain-text-splitters")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    chunks = splitter.split_documents(documents)

    print("\nYouTube chunks:", len(chunks))
    for number, chunk in enumerate(chunks[:5], start=1):
        print(f"\nChunk {number}")
        print("Metadata:", chunk.metadata)
        print("Text:", chunk.page_content[:500])

    return chunks


def task_8_youtube_vector_store(chunks):
    print("\n" + "=" * 70)
    print("TASK 8 - OpenAI Embeddings + FAISS for YouTube")
    print("=" * 70)

    if not chunks:
        print("No YouTube chunks available.")
        return None

    vector_store = build_vector_store(chunks)

    if vector_store is None:
        return None

    query = "What is the main topic discussed in this video?"
    results = vector_store.similarity_search(query, k=4)

    print("Query:", query)
    for number, document in enumerate(results, start=1):
        print(f"\nResult {number}")
        print(document.page_content[:700])

    save_directory = OUTPUT_DIR / "youtube_faiss_index"

    try:
        vector_store.save_local(str(save_directory))
        print("\nFAISS index saved at:", save_directory)
    except Exception as error:
        print("Could not save FAISS index:", error)

    return vector_store


def make_rag_chain(vector_store, model):
    if vector_store is None or model is None:
        return None

    from langchain_core.prompts import ChatPromptTemplate

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful YouTube-video assistant.

Answer the user's question using ONLY the retrieved transcript context.
If the answer is not present in the context, say that the video transcript
does not provide enough information.

Retrieved context:
{context}
"""
            ),
            ("human", "{question}")
        ]
    )

    def answer_question(question):
        documents = retriever.invoke(question)
        context = "\n\n".join(
            document.page_content for document in documents
        )

        response = model.invoke(
            prompt.format_messages(
                context=context,
                question=question
            )
        )

        return response.content, documents

    return answer_question


def task_9_build_youtube_chatbot(vector_store, model):
    print("\n" + "=" * 70)
    print("TASK 9 - Build YouTube RAG Chatbot")
    print("=" * 70)

    rag_function = make_rag_chain(vector_store, model)

    if rag_function is None:
        print("YouTube RAG chatbot could not be created.")
        return None

    print("RAG chatbot is ready.")
    print("It retrieves transcript chunks first and then sends only retrieved")
    print("context to the OpenAI model.")

    return rag_function


def task_10_testing_evaluation(rag_function):
    print("\n" + "=" * 70)
    print("TASK 10 - Testing & Evaluation")
    print("=" * 70)

    if rag_function is None:
        print("RAG function is unavailable.")
        return []

    questions = [
        "What is the main topic of the video?",
        "What are the most important points discussed?",
        "Give one example mentioned in the video.",
        "What conclusion does the speaker make?",
        "Summarize the video in a few sentences."
    ]

    results = []

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}: {question}")

        try:
            answer, documents = rag_function(question)

            print("Retrieved chunks:", len(documents))
            print("Answer:", answer)

            results.append(
                {
                    "question": question,
                    "answer": answer,
                    "retrieved_chunks": len(documents)
                }
            )

        except Exception as error:
            print("Question failed:", error)

    return results


# ============================================================
# PART 5 - Observations & Insights
# ============================================================

def task_11_conceptual_questions():
    print("\n" + "=" * 70)
    print("TASK 11 - Conceptual Questions")
    print("=" * 70)

    answers = {
        "1. Retriever-based RAG vs normal prompting":
            "Normal prompting gives the model only the prompt and its learned knowledge. "
            "Retriever-based RAG first searches an external knowledge source and supplies "
            "relevant context to the model.",

        "2. Why vector stores are critical":
            "Vector stores make it practical to save embeddings and search large collections "
            "of documents using semantic similarity instead of checking every document manually.",

        "3. When to use MMR":
            "MMR is useful when relevant results may be very similar to one another. "
            "It balances relevance with diversity.",

        "4. Benefits of multi-query retrieval":
            "Multi-query retrieval asks the LLM to create alternative versions of a query. "
            "Different phrasings can retrieve information that a single query might miss.",

        "5. Importance of contextual compression":
            "Compression reduces irrelevant parts of retrieved documents before they are "
            "sent to the LLM, helping keep the context focused and reducing unnecessary tokens."
    }

    for question, answer in answers.items():
        print("\n" + question)
        print(answer)

    return answers


def save_run_results(results):
    import json

    path = OUTPUT_DIR / "TEST_RESULTS.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("\nSaved test results to:", path)


def main():
    print("Assignment 23 - OpenAI & Retrieval-Augmented Generation (RAG)")

    model = task_1_openai_basic_prompt()

    wikipedia_documents = task_2_wikipedia_retriever()
    vector_store = task_3_vector_store_retriever(wikipedia_documents)

    task_4_mmr_retriever(vector_store)
    task_5_multi_query_retriever(vector_store, model)
    task_6_contextual_compression(vector_store, model)

    youtube_documents = task_7_load_youtube_transcript()
    youtube_chunks = split_youtube_documents(youtube_documents)
    youtube_store = task_8_youtube_vector_store(youtube_chunks)

    rag_function = task_9_build_youtube_chatbot(youtube_store, model)
    results = task_10_testing_evaluation(rag_function)

    task_11_conceptual_questions()

    if results:
        save_run_results(results)

    print("\nAssignment 23 execution finished.")


if __name__ == "__main__":
    main()
