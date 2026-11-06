# Assignment 27 - Chatbots with Conversation History using LangChain

## What was fixed

1. Added separate written answers for Task 1.
2. Added a 2-3 turn follow-up demonstration in `main.py`.
3. Added message-count trimming.
4. Added approximate token-length trimming in `trim_history_by_tokens()`.
5. Added a Streamlit conversation interface.
6. Added a notebook with Tasks 1-7 separated into sections.
7. Added clear run instructions.
8. Added an `outputs` folder for the student's real Streamlit screenshot.
9. Kept `MY_RUN_NOTES.txt` as a real-execution record instead of inventing responses.

## Requirements

- Python 3.10+
- Ollama installed locally
- A model such as `llama3.2`

Install Python packages:

```bash
pip install -r requirements.txt
```

Pull and start the model:

```bash
ollama pull llama3.2
ollama list
```

Ollama normally runs as a local service. If it is not running, start it with:

```bash
ollama serve
```

## Run the terminal chatbot

```bash
python main.py
```

Expected test questions:

1. Explain Python lists in simple words.
2. Give me one example.
3. What about tuples?

Record the actual responses, model name, errors and fixes in `MY_RUN_NOTES.txt`.

## Run Streamlit

```bash
streamlit run app.py
```

Ask the same three questions in the browser. Take a screenshot of the actual
conversation and save it as:

`outputs/streamlit_chatbot.png`

The screenshot must be your real execution evidence. Do not create a fake image.

## Task 1 - message types

- `SystemMessage`: instructions that guide the assistant.
- `HumanMessage`: a message sent by the user.
- `AIMessage`: a previous response from the assistant.

Message-based prompts keep the conversation roles separate. This makes it
easier to send system instructions together with previous user/assistant turns.

## Task 4 - history limits

The project demonstrates two simple limits:

- `trim_history()` keeps only the most recent messages.
- `trim_history_by_tokens()` estimates token size from character length and
  keeps recent messages until the chosen limit is reached.

The second method is only an approximation because the exact tokenizer can
differ between models.

## Important

Do not invent execution output. Fill `MY_RUN_NOTES.txt` only after running the
program locally and add the real screenshot to `outputs/`.
