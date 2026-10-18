# Assignment 38: CodeLlama with Ollama

A local coding assistant powered by **CodeLlama** running through **Ollama**.
It can generate Python code, explain code, debug errors and suggest optimizations,
through Python functions and a Streamlit app. Everything runs on your own machine
(no cloud API, no API key).

## Project structure
| File | Task |
|------|------|
| `check_setup.py` | Task 1: verify Ollama is running and the model is pulled |
| `task2_basic_interaction.py` | Task 2: send prompts with the Ollama Python library and the LangChain wrapper |
| `code_assistant.py` | Tasks 3 and 5: assistant functions + prompt templates |
| `task3_demo.py` | Task 3: demo of generation, explanation, bug fixing and optimization |
| `app.py` | Task 4: Streamlit code assistant app |
| `test_offline.py` | Logic test with a fake LLM (needs no Ollama) |
| `.env.example` | Optional settings (model name, Ollama host) |

## Task 1 – Setup CodeLlama with Ollama
1. **Install Ollama:** download from https://ollama.com/download (Windows/macOS installer;
   Linux: `curl -fsSL https://ollama.com/install.sh | sh`).
2. **Pull the model** (about 3.8 GB download):
   ```bash
   ollama pull codellama:7b
   ```
3. **Verify it is running:**
   ```bash
   ollama list                                  # codellama:7b should be listed
   ollama run codellama:7b "Say hello"          # quick manual test
   python check_setup.py                        # automatic check
   ```
   Ollama runs as a background server on `http://localhost:11434`. If it is not running, start the
   Ollama app or run `ollama serve`. CodeLlama 7B needs about 8 GB of RAM (a GPU makes it faster but is optional).

## How to run
```bash
pip install -r requirements.txt
python check_setup.py               # Task 1
python task2_basic_interaction.py   # Task 2
python task3_demo.py                # Task 3
streamlit run app.py                # Task 4 (the app)
```

## Task 2 – Basic CodeLlama interaction
`task2_basic_interaction.py` sends two prompts, "Write a Python function to check prime numbers" and
"Explain this code" (with a sample snippet), using both the **Ollama Python library** (`ollama.Client.chat`)
and the **LangChain wrapper** (`ChatOllama`), and prints the responses.

## Task 3 – Code assistant features (`code_assistant.py`)
| Function | What it does |
|----------|--------------|
| `generate_code(description)` | Writes code from a plain-English request |
| `explain_code(code)` | Explains code step by step for a beginner |
| `fix_bug(code, error="")` | Finds the bug, returns fixed code and what changed |
| `optimize_code(code)` | Lists issues and returns an improved version with complexity before/after |

## Task 4 – Streamlit app
- **Text area** for code or a prompt (plus an optional error-message box in Debug mode).
- **Dropdown** for the task type: Generate Code, Explain Code, Debug Code, Optimize Code.
- The answer is **displayed live** (streamed) as formatted Markdown with code blocks, can be
  downloaded as `.md`, and earlier results of the session are kept in a "Previous results" section.
- The sidebar shows whether Ollama is running and the model is available, with a temperature slider.
  If Ollama is not running, the app shows a clear message instead of crashing.

## Task 5 – Prompt engineering for CodeLlama
Each task type has its own `ChatPromptTemplate` (system role + human message). To make outputs clear,
structured and readable, every template:
- gives the model a **role** (Python expert / teacher / senior engineer / performance expert);
- demands **fixed Markdown section headings**, so output always looks the same:

| Task | Sections |
|------|----------|
| Generate | Code, How it works, Example usage |
| Explain | Summary, Step-by-step, Key concepts, Complexity |
| Debug | Problem found, Fixed code, What changed, How to avoid it |
| Optimize | Issues found, Optimized code, Why it is better, Complexity |

- requires code in fenced ```python blocks, and asks for concise answers without filler;
- uses a low temperature (0.2) for consistent, reliable code.

## Notes
- `test_offline.py` passes here: every prompt template renders, the four assistant functions and
  streaming work, a missing Ollama server is handled gracefully, and the Streamlit app runs end to end
  (Debug mode shows the extra error box and the result is saved to the session history). It used a fake
  LLM, because Ollama and CodeLlama are not available in my environment.
- Answer quality and speed come from CodeLlama 7B on your computer. Small models can make mistakes,
  so always read and test the generated code. For better answers try `OLLAMA_MODEL=codellama:13b` in `.env`.
- Screenshots for submission: `ollama list` output, `check_setup.py`, and the Streamlit app showing each of the four task types.
