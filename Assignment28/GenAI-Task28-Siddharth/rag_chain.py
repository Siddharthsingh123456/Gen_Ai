"""PART 4 - Task 6 & 7: the conversational RAG chain.

User Question -> (rewrite with history) -> Retriever -> Context -> Prompt -> LLM -> Answer
                                                          ^ history injected via MessagesPlaceholder
"""
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from history import ChatHistory
from prompts import CONTEXTUALIZE_PROMPT, QA_PROMPT


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in docs
    )


def build_rag_chain(llm, retriever):
    """Build the LCEL chain. Input: {"question": str, "chat_history": [messages]}."""
    parser = StrOutputParser()
    rewrite = CONTEXTUALIZE_PROMPT | llm | parser

    def standalone_question(inputs: dict) -> str:
        # No history -> the question is already standalone (saves one LLM call).
        if not inputs["chat_history"]:
            return inputs["question"]
        return rewrite.invoke(inputs)

    chain = (
        RunnablePassthrough.assign(standalone=RunnableLambda(standalone_question))
        | RunnablePassthrough.assign(
            docs=RunnableLambda(lambda x: retriever.invoke(x["standalone"]))
        )
        | RunnablePassthrough.assign(context=RunnableLambda(lambda x: format_docs(x["docs"])))
        | RunnablePassthrough.assign(answer=QA_PROMPT | llm | parser)
    )
    return chain


class ConversationalRAG:
    """Chat wrapper: runs the chain and keeps message history between turns."""

    def __init__(self, llm, retriever, history_mode: str = "messages"):
        self.chain = build_rag_chain(llm, retriever)
        self.history = ChatHistory(mode=history_mode)

    def ask(self, question: str) -> Tuple[str, List[Document]]:
        result = self.chain.invoke(
            {"question": question, "chat_history": self.history.messages}
        )
        self.history.add_interaction(question, result["answer"])   # Task 7
        return result["answer"], result["docs"]

    def reset(self) -> None:
        self.history.clear()
