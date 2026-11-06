"""PART 4 - Tasks 6 & 7: conversational RAG chain with message history.

User Question -> (rewrite using history) -> Retriever -> PDF Context
              -> Prompt + Message History (MessagesPlaceholder) -> LLM -> Answer
"""
from typing import Iterator, List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from history import ChatHistory
from prompts import CONTEXTUALIZE_PROMPT, QA_PROMPT


def page_of(doc: Document) -> int:
    """PyPDFLoader pages are 0-based; humans count from 1."""
    return int(doc.metadata.get("page", 0)) + 1


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(
        f"[{d.metadata.get('source', 'pdf')}, page {page_of(d)}]\n{d.page_content}" for d in docs
    )


def _prepare_chain(llm, retriever):
    parser = StrOutputParser()
    rewrite = CONTEXTUALIZE_PROMPT | llm | parser

    def standalone(inputs: dict) -> str:
        if not inputs["chat_history"]:           # first turn: nothing to resolve
            return inputs["question"]
        return rewrite.invoke(inputs)

    return (
        RunnablePassthrough.assign(standalone=RunnableLambda(standalone))
        | RunnablePassthrough.assign(docs=RunnableLambda(lambda x: retriever.invoke(x["standalone"])))
        | RunnablePassthrough.assign(context=RunnableLambda(lambda x: format_docs(x["docs"])))
    )


def build_rag_chain(llm, retriever):
    """Task 6: the complete chain. Input: {"question": str, "chat_history": [messages]}."""
    return _prepare_chain(llm, retriever) | RunnablePassthrough.assign(
        answer=QA_PROMPT | llm | StrOutputParser()
    )


class ConversationalPDFChat:
    """Runs the chain and maintains (and trims) the message history between turns (Tasks 7-8)."""

    def __init__(self, llm, retriever, history_mode: str = "messages"):
        self.prep = _prepare_chain(llm, retriever)
        self.answer_chain = QA_PROMPT | llm | StrOutputParser()
        self.chain = build_rag_chain(llm, retriever)
        self.history = ChatHistory(mode=history_mode)
        self.last_docs: List[Document] = []

    def ask(self, question: str):
        result = self.chain.invoke({"question": question, "chat_history": self.history.messages})
        self.history.add_interaction(question, result["answer"])       # Task 7 (+ Task 8 trimming)
        self.last_docs = result["docs"]
        return result["answer"], result["docs"]

    def ask_stream(self, question: str) -> Iterator[str]:
        """Same as ask() but yields the answer token by token (used by the Streamlit UI)."""
        inputs = self.prep.invoke({"question": question, "chat_history": self.history.messages})
        self.last_docs = inputs["docs"]
        parts: List[str] = []
        for token in self.answer_chain.stream(inputs):
            parts.append(token)
            yield token
        self.history.add_interaction(question, "".join(parts))

    def reset(self) -> None:
        self.history.clear()
