"""PART 3 - Task 5: RAG prompt template with message history."""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

NOT_FOUND = "I don't know."

# 1) System message (RAG instructions)  2) MessagesPlaceholder  3) Human question
QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Document Q&A assistant.\n"
            "Answer ONLY using the retrieved context below. Do not use outside knowledge.\n"
            f"If the answer is not in the context, reply exactly: \"{NOT_FOUND}\"\n"
            "Use the chat history only to understand follow-up questions such as "
            "'Explain more' or 'What about the previous point?'.\n"
            "Be clear and concise.\n\n"
            "Retrieved context:\n{context}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

# Helper prompt: turns a follow-up into a standalone search query, so the
# retriever finds the right chunks for questions like "Explain more".
CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user question, rewrite the question "
            "as a standalone question that can be understood without the history. "
            "Do NOT answer it. If it is already standalone, return it unchanged.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
