"""
Assignment 21: LangChain Document Loaders & Text Splitters

Run:
    python main.py

The script uses the real LangChain packages. It does not contain mock loader classes.
If a required package is missing, install requirements.txt and run again.
"""

from pathlib import Path
import sys
import traceback

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def main():
    try:
        from langchain_community.document_loaders import (
            TextLoader, CSVLoader, PyPDFLoader, DirectoryLoader, WebBaseLoader
        )
        from langchain_text_splitters import (
            CharacterTextSplitter,
            RecursiveCharacterTextSplitter,
            MarkdownHeaderTextSplitter,
        )
    except Exception as exc:
        print("REAL LANGCHAIN IMPORT FAILED")
        print(type(exc).__name__ + ":", exc)
        print("\nInstall the dependencies first:")
        print("python -m pip install -r requirements.txt")
        return 1

    print("REAL LANGCHAIN MODE")
    print("Python:", sys.version.split()[0])

    # Task 1
    section("TASK 1 - TEXT LOADER")
    text_loader = TextLoader(str(DATA / "sample.txt"), encoding="utf-8")
    text_docs = text_loader.load()
    print("Number of documents:", len(text_docs))
    print("Preview:", text_docs[0].page_content[:250].replace("\n", " "))
    print("Metadata:", text_docs[0].metadata)

    # Task 2
    section("TASK 2 - CSV LOADER")
    csv_docs = CSVLoader(str(DATA / "sample.csv")).load()
    print("CSV rows converted to documents:", len(csv_docs))
    for i, doc in enumerate(csv_docs[:3], 1):
        print(f"Row {i}:", doc.page_content)

    # Task 3
    section("TASK 3 - PDF LOADER")
    pdf_docs = PyPDFLoader(str(DATA / "sample.pdf")).load()
    print("PDF pages loaded:", len(pdf_docs))
    print("PDF content preview:", pdf_docs[0].page_content[:350].replace("\n", " "))
    print("PDF metadata:", pdf_docs[0].metadata)

    # Task 4
    section("TASK 4 - DIRECTORY LOADER")
    directory_loader = DirectoryLoader(
        str(DATA), glob="*.txt", loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    directory_docs = directory_loader.load()
    print("TXT documents loaded from directory:", len(directory_docs))
    print("Loaded files:", [d.metadata.get("source") for d in directory_docs])

    # Task 5
    section("TASK 5 - WEBBASELOADER")
    try:
        web_docs = WebBaseLoader("https://example.com").load()
        print("Web documents loaded:", len(web_docs))
        web_text = web_docs[0].page_content
        print("First 500 characters:")
        print(web_text[:500])
    except Exception as exc:
        print("Web loader could not reach the website in this environment.")
        print(type(exc).__name__ + ":", exc)
        print("The local loader tasks are still independent of this network issue.")

    # Task 6
    section("TASK 6 - WHY TEXT SPLITTING IS REQUIRED")
    print(
        "Large documents may exceed an LLM context window. Splitting creates smaller "
        "retrievable units, reduces irrelevant context, and makes retrieval more precise."
    )
    print(
        "A chunk should be large enough to preserve meaning but small enough to fit "
        "comfortably inside the model's token/context limits."
    )

    # Task 7
    section("TASK 7 - CHARACTER TEXT SPLITTER")
    character_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=180, chunk_overlap=30
    )
    character_chunks = character_splitter.split_documents(text_docs)
    print("Number of character chunks:", len(character_chunks))
    for i, chunk in enumerate(character_chunks[:3], 1):
        print(f"Chunk {i}:", chunk.page_content[:180].replace("\n", " "))

    # Task 8
    section("TASK 8 - RECURSIVE CHARACTER TEXT SPLITTER")
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=180, chunk_overlap=30
    )
    recursive_chunks = recursive_splitter.split_documents(text_docs)
    print("Number of recursive chunks:", len(recursive_chunks))
    for i, chunk in enumerate(recursive_chunks[:3], 1):
        print(f"Chunk {i}:", chunk.page_content[:180].replace("\n", " "))
    print("\nComparison:")
    print("- CharacterTextSplitter follows the chosen separator.")
    print("- RecursiveCharacterTextSplitter tries several separators and usually keeps")
    print("  words/sentences more naturally when the first separator is not suitable.")

    # Task 9
    section("TASK 9 - MARKDOWN HEADER TEXT SPLITTER")
    markdown_text = (DATA / "sample.md").read_text(encoding="utf-8")
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2")]
    )
    markdown_chunks = header_splitter.split_text(markdown_text)
    print("Structured markdown chunks:", len(markdown_chunks))
    for i, chunk in enumerate(markdown_chunks[:4], 1):
        print(f"Chunk {i} metadata:", chunk.metadata)
        print(f"Chunk {i} text:", chunk.page_content[:160].replace("\n", " "))

    # Task 10
    section("TASK 10 - SEMANTIC SPLITTING (OPTIONAL)")
    print(
        "Semantic splitting groups text using meaning/similarity rather than only "
        "character boundaries. It can be useful when topic boundaries matter."
    )
    try:
        from langchain_experimental.text_splitter import SemanticChunker
        from langchain_openai import OpenAIEmbeddings
        print("SemanticChunker package is available.")
        print("Demo is optional because it requires an embeddings API key.")
    except Exception as exc:
        print("Optional SemanticChunker demo not run:", type(exc).__name__)
        print("Conceptual explanation supplied above.")

    # Task 11
    section("TASK 11 - UNIFIED load_and_split_documents(path_or_url)")
    def load_and_split_documents(path_or_url):
        """Load a local directory/file or URL, then return recursive chunks."""
        if str(path_or_url).startswith(("http://", "https://")):
            documents = WebBaseLoader(str(path_or_url)).load()
        else:
            path = Path(path_or_url)
            if path.is_dir():
                documents = DirectoryLoader(
                    str(path), glob="*.txt", loader_cls=TextLoader,
                    loader_kwargs={"encoding": "utf-8"}
                ).load()
            elif path.suffix.lower() == ".pdf":
                documents = PyPDFLoader(str(path)).load()
            elif path.suffix.lower() == ".csv":
                documents = CSVLoader(str(path)).load()
            else:
                documents = TextLoader(str(path), encoding="utf-8").load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=180, chunk_overlap=30)
        return splitter.split_documents(documents)

    local_result = load_and_split_documents(DATA)
    print("Local directory chunks:", len(local_result))
    print("Local sample:", local_result[0].page_content[:180].replace("\n", " "))

    try:
        url_result = load_and_split_documents("https://example.com")
        print("Web URL chunks:", len(url_result))
        print("Web sample:", url_result[0].page_content[:180].replace("\n", " "))
    except Exception as exc:
        print("Web URL test could not run because of network access:", exc)

    # Task 12
    section("TASK 12 - OBSERVATIONS & INSIGHTS")
    print("1. TextLoader is suitable for plain text files.")
    print("2. CSVLoader is suitable when each row should become a document.")
    print("3. PyPDFLoader is useful for page-oriented PDF extraction.")
    print("4. DirectoryLoader is useful for processing many files together.")
    print("5. WebBaseLoader is useful for public web pages when network access is available.")
    print("6. RecursiveCharacterTextSplitter is a good general-purpose choice for prose.")
    print("7. MarkdownHeaderTextSplitter is better when section/header structure matters.")
    print("8. Chunk overlap preserves context when an important sentence crosses boundaries.")
    print("9. Chunk size must balance retrieval precision with the LLM context/token limit.")
    print("10. Semantic splitting can help when meaning/topic boundaries are more important")
    print("    than fixed character boundaries.")

    print("\nALL AVAILABLE TASKS EXECUTED WITH REAL LANGCHAIN.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
