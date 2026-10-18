# Assignment 29 - Q&A Chatbot Application

## What was fixed

1. Added the required `get_answer(question, model_type="openai")` function.
2. Added one model-switching function for OpenAI and Ollama.
3. Used `ChatPromptTemplate`.
4. Used `MessagesPlaceholder` for conversation history.
5. Added `app.py` with a Streamlit model selector.
6. Added error handling for missing API keys/Ollama.
7. Added `.env.example` and requirements.

## Setup

### OpenAI

Copy `.env.example` to `.env` and add your real OpenAI API key.

### Ollama

Install Ollama and run:

```bash
ollama pull llama3.2
```

Then make sure Ollama is running.

### Install packages

```bash
pip install -r requirements.txt
```

## Run CLI

```bash
python main.py
```

Choose `openai` or `ollama`, then ask questions.

## Run Streamlit

```bash
streamlit run app.py
```

Choose the model in the sidebar area and ask questions.

## Task 7

The required function is:

```python
get_answer(question, model_type="openai")
```

It selects the requested model and sends the question together with the stored conversation history.

## Evidence

The files inside `outputs/` are intentionally not filled with invented model responses. Run the application yourself and save the real output/screenshots there before submission.
