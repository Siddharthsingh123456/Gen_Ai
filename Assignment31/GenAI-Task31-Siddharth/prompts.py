"""PART 3 - Task 5: conversational RAG prompt template."""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

NOT_FOUND = "I don't know."

# 1) System message (answer from PDF only)  2) MessagesPlaceholder (chat history)  3) Human question
QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a PDF Q&A assistant.\n"
            "Answer ONLY using the retrieved PDF context below. Do not use outside knowledge.\n"
            f"If the answer is not in the PDF context, reply exactly: \"{NOT_FOUND}\"\n"
            "Use the chat history only to understand follow-up questions such as "
            "'explain more' or 'what about the previous topic?'.\n"
            "Mention the page number when it helps. Be clear and concise.\n\n"
            "Retrieved PDF context:\n{context}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

# Rewrites a follow-up into a standalone search query so the retriever finds the right PDF chunks.
CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user question, rewrite the question as a "
            "standalone question that can be understood without the history. "
            "Do NOT answer it. If it is already standalone, return it unchanged.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
