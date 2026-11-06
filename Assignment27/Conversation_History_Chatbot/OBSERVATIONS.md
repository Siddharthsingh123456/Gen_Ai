# Task 7 - Observations & Insights

## 1. Why is chat history important?

Chat history gives the model the earlier user and assistant messages. This is
needed for follow-up questions such as "Give an example" because that question
depends on the earlier topic.

## 2. Trade-off between long memory and performance

More history gives the model more context, but it also sends more text to the
model. This can increase token usage and response time. A practical chatbot
therefore needs a limit.

## 3. When should history be summarized vs trimmed?

Trimming is useful when only recent messages matter. Summarization is better
when older information is important and should be kept in a shorter form.

## 4. Message placeholders vs memory

`MessagesPlaceholder` is a position in a prompt where previous messages are
inserted. It does not store messages by itself. In this project,
`st.session_state.history` or the Python `history` list stores the messages,
while the placeholder sends them to the model.

## 5. What the follow-up test should demonstrate

The three questions are:

- Explain Python lists in simple words.
- Give me one example.
- What about tuples?

The second and third questions should make sense because earlier messages are
included in the prompt.

## 6. Why token limits matter

A model has a finite context window. Sending a very large conversation can
increase cost/time and may eventually exceed the model's context capacity.
The project therefore includes both message-count and approximate token
limits.

**Execution-specific observations must be added to `MY_RUN_NOTES.txt` after
running the project.**
