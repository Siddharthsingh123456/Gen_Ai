"""CodeLlama code assistant (runs locally through Ollama).

Contains: connection check, prompt templates (Task 5) and the four assistant
functions (Task 3): generate, explain, debug/fix, optimize.
"""
import json
import os
import urllib.request
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
MODEL = os.getenv("OLLAMA_MODEL", "codellama:7b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


# ----------------------------------------------------------------- Ollama connection
def check_ollama(host: str = HOST, model: str = MODEL):
    """Return (is_running, model_is_pulled, installed_models)."""
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=3) as resp:
            tags = json.load(resp)
    except Exception:
        return False, False, []
    names = [m["name"] for m in tags.get("models", [])]
    pulled = any(n == model or n.split(":")[0] == model.split(":")[0] and ":" not in model for n in names)
    return True, pulled, names


def get_llm(model: str = MODEL, temperature: float = 0.2):
    from langchain_ollama import ChatOllama
    return ChatOllama(model=model, base_url=HOST, temperature=temperature)


# ----------------------------------------------------------------- Prompt templates (Task 5)
# One template per task type. Each asks for a clear, structured, readable answer.
_STYLE = ("Format the answer in Markdown using exactly the section headings given below. "
          "Put all code in fenced ```python blocks. Be concise and clear; avoid filler text.")

PROMPTS = {
    "Generate Code": ChatPromptTemplate.from_messages([
        ("system", "You are an expert Python developer. " + _STYLE +
         "\n\nSections:\n## Code\n(complete, working code with docstrings and type hints)\n"
         "## How it works\n(2-4 bullet points)\n## Example usage\n(a short runnable example with expected output)"),
        ("human", "Write Python code for this request:\n{user_input}"),
    ]),
    "Explain Code": ChatPromptTemplate.from_messages([
        ("system", "You are a patient programming teacher explaining code to a beginner. " + _STYLE +
         "\n\nSections:\n## Summary\n(one sentence: what the code does)\n"
         "## Step-by-step\n(numbered list, one step per line or block of code)\n"
         "## Key concepts\n(bullet list of the concepts used)\n## Complexity\n(time and space, if relevant)"),
        ("human", "Explain this code:\n```python\n{user_input}\n```"),
    ]),
    "Debug Code": ChatPromptTemplate.from_messages([
        ("system", "You are a senior engineer who finds and fixes bugs. " + _STYLE +
         "\n\nSections:\n## Problem found\n(what is wrong and on which line)\n"
         "## Fixed code\n(the complete corrected code)\n## What changed\n(bullet list)\n"
         "## How to avoid it\n(one short tip)"),
        ("human", "Debug this code.\n\nCode:\n```python\n{user_input}\n```\n\n"
                  "Error message or unexpected behaviour (may be empty):\n{error}"),
    ]),
    "Optimize Code": ChatPromptTemplate.from_messages([
        ("system", "You are a performance and code-quality expert. " + _STYLE +
         "\n\nSections:\n## Issues found\n(bullet list: speed, memory, readability)\n"
         "## Optimized code\n(the complete improved code)\n"
         "## Why it is better\n(bullet list)\n## Complexity\n(before vs after)"),
        ("human", "Suggest improvements and optimize this code:\n```python\n{user_input}\n```"),
    ]),
}
TASKS = list(PROMPTS)


def _variables(task: str, user_input: str, error: str = "") -> dict:
    vars_ = {"user_input": user_input.strip()}
    if task == "Debug Code":
        vars_["error"] = error.strip() or "(none given - find any bugs yourself)"
    return vars_


def run_task(task: str, user_input: str, error: str = "", llm=None) -> str:
    """Run one assistant task and return the full response."""
    chain = PROMPTS[task] | (llm or get_llm()) | StrOutputParser()
    return chain.invoke(_variables(task, user_input, error))


def stream_task(task: str, user_input: str, error: str = "", llm=None):
    """Same as run_task but yields the answer piece by piece (for live display)."""
    chain = PROMPTS[task] | (llm or get_llm()) | StrOutputParser()
    yield from chain.stream(_variables(task, user_input, error))


# ----------------------------------------------------------------- Task 3: assistant functions
def generate_code(description: str, llm=None) -> str:
    return run_task("Generate Code", description, llm=llm)


def explain_code(code: str, llm=None) -> str:
    return run_task("Explain Code", code, llm=llm)


def fix_bug(code: str, error: str = "", llm=None) -> str:
    return run_task("Debug Code", code, error, llm=llm)


def optimize_code(code: str, llm=None) -> str:
    return run_task("Optimize Code", code, llm=llm)
