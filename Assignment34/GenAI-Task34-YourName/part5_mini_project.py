"""PART 5 - Mini project: reusable summarization function (Tasks 13-14). Task 14 is in Readme.md."""
import argparse
from summarizer import *


def summarize_document(text: str, method: str = "map_reduce", llm=None,
                       chunk_size: int = 2000, chunk_overlap: int = 200) -> str:
    """Return a summary of `text` using one of: prompt | stuff | map_reduce | refine."""
    llm = llm or get_llm()
    method = method.lower().replace("-", "_")
    if method == "prompt":
        return prompt_summary(llm, text, SHORT_PROMPT)
    if method == "stuff":
        return stuff_summary(llm, [Document(page_content=text)])
    if method == "map_reduce":
        return map_reduce_summary(llm, split_text(text, chunk_size, chunk_overlap))
    if method == "refine":
        return refine_summary(llm, split_text(text, chunk_size, chunk_overlap))
    raise ValueError("method must be one of: prompt, stuff, map_reduce, refine")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Summarize a document with LangChain")
    p.add_argument("--method", default="map_reduce",
                   choices=["prompt", "stuff", "map_reduce", "refine"])
    p.add_argument("--file", default=DOC_PATH, help=".txt or .pdf file")
    args = p.parse_args()

    doc_text = load_text(args.file)
    print(f"Method: {args.method} | characters: {len(doc_text)}\n")
    result, secs = timed(summarize_document, doc_text, args.method)
    print(result, f"\n\n(time: {secs}s)")
    save_output(f"part5_{args.method}.txt", result)
