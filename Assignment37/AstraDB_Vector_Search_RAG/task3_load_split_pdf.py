"""TASK 3 - Load a PDF with LangChain's PDF loader, split the text into chunks, prepare for embedding."""
import sys
from rag_core import load_pdf, split_documents

path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.pdf"
pages = load_pdf(path)                                   # 1. PyPDFLoader
print(f"Loaded '{path}': {len(pages)} page(s), {sum(len(p.page_content) for p in pages)} characters")

chunks = split_documents(pages, chunk_size=1000, chunk_overlap=150)   # 2. RecursiveCharacterTextSplitter
sizes = [len(c.page_content) for c in chunks]
print(f"Split into {len(chunks)} chunks | min {min(sizes)} / avg {sum(sizes)//len(sizes)} / max {max(sizes)} characters")

print("\n3. Prepared documents (text + metadata) ready for embedding:")        # 3. preview
for c in chunks[:3]:
    print(f"\n--- metadata={c.metadata}\n{c.page_content[:300]}...")
