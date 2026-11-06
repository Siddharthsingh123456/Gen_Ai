"""PART 4 - Task 7 & 8: message history storage and trimming."""
from typing import List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, trim_messages

import config


def approx_token_counter(messages: List[BaseMessage]) -> int:
    """Cheap token estimate (~4 characters per token) - no extra dependency."""
    return sum(len(str(m.content)) // 4 + 4 for m in messages)


def trim_history(messages: List[BaseMessage], mode: str = config.TRIM_MODE) -> List[BaseMessage]:
    """Drop the OLDEST messages once the limit is exceeded.

    mode="messages": keep at most MAX_HISTORY_MESSAGES messages.
    mode="tokens"  : keep at most MAX_HISTORY_TOKENS (approximate) tokens.
    The kept history always starts with a human message.
    """
    if mode == "tokens":
        counter, limit = approx_token_counter, config.MAX_HISTORY_TOKENS
    else:
        counter, limit = len, config.MAX_HISTORY_MESSAGES

    return trim_messages(
        messages,
        max_tokens=limit,
        token_counter=counter,
        strategy="last",      # keep the newest messages
        start_on="human",
        include_system=False,
        allow_partial=False,
    )


class ChatHistory:
    """Stores user + AI messages after every interaction (Task 7)."""

    def __init__(self, mode: str = config.TRIM_MODE):
        self.mode = mode
        self.messages: List[BaseMessage] = []

    def add_interaction(self, question: str, answer: str) -> None:
        self.messages.append(HumanMessage(content=question))
        self.messages.append(AIMessage(content=answer))
        self.messages = trim_history(self.messages, self.mode)   # Task 8

    def clear(self) -> None:
        self.messages = []
