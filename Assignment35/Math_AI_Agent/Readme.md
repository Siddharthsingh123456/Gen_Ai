# Assignment 35: Text-to-Math Agent

A GenAI assistant that solves math word problems step by step. It uses a LangChain
agent, an LLM (Groq / OpenAI / Ollama), math tools (calculator + algebra solver) and
Streamlit session state, so it remembers the conversation.

## Project structure
| File | Purpose |
|------|---------|
| `math_tools.py` | Task 2 tools: safe `calculator` and `solve_equation` (SymPy) |
| `math_agent.py` | Task 2 agent: LLM + tools + system prompt; `solve()` returns answer + tool calls; has a CLI chat |
| `app.py` | Task 3 Streamlit app using `st.session_state` |
| `test_agent.py` | Task 2 tests: arithmetic, percentage and algebra problems + memory test |
| `.env.example` | Copy to `.env` and add your key |

## How to run
```bash
pip install -r requirements.txt
cp .env.example .env                  # add GROQ_API_KEY (or OPENAI_API_KEY, or use ollama)

python test_agent.py                  # tool tests + agent tests on sample problems
streamlit run app.py                  # the web application
python math_agent.py                  # optional: terminal chat
```

## Task 1 – Text-to-Math Agent Overview

**1. What is a Text-to-Math problem?**
A problem written in natural language (a word problem such as "A shirt costs 80 and has
25% off, what do I pay?") that must be converted into mathematical operations or equations,
solved, and answered. It needs both language understanding and exact calculation.

**2. Why are agents useful for math reasoning?**
LLMs predict text, so they can make arithmetic mistakes, especially with large numbers or
multi-step problems. An agent lets the LLM *reason* about the problem and *delegate* exact
calculation to tools (calculator, equation solver). It can break the problem into steps,
call tools repeatedly, check results, and keep memory of earlier answers.

**3. Normal LLM response vs agent-based reasoning?**

| | Normal LLM response | Agent-based reasoning |
|---|---|---|
| Calculation | Done "in the head" by text prediction, can be wrong | Done by tools, exact |
| Process | One-shot answer | Loop: think, call tool, observe, continue |
| Multi-step problems | Prone to drifting or errors | Handled step by step |
| Verifiability | Hard to check | Tool calls are visible and can be inspected |
| Memory/context | Only what is in the prompt | Can use stored session state and tools |

## Task 2 – How the agent works
- **Math tools:** `calculator` (arithmetic, percentages, sqrt, powers) and `solve_equation`
  (algebra, e.g. `3*x + 7 = 25`). The calculator parses expressions with Python's `ast`
  module instead of `eval()`, so arbitrary code cannot be executed (tested).
- **LLM:** Groq, OpenAI or Ollama (set `LLM_PROVIDER` in `.env`).
- **Agent behaviour (system prompt):** understands the word problem, breaks it into steps,
  uses tools for every calculation, and ends with `Final Answer: ...`.
- **Tests (`test_agent.py`):**
  - Arithmetic word problem: 7 notebooks at 45 + 3 pens at 12 -> 351
  - Percentage problem: 15% discount on 20000 -> discount 3000, price 17000
  - Simple algebra: 3x + 7 = 25 -> x = 6
  - Memory test: "Now multiply the last answer by 2" uses the previous answer.

## Task 3 – Session state in Streamlit
`app.py` uses `st.session_state` to:
1. **Maintain conversation history:** `messages` is displayed in the chat and replayed on every rerun.
2. **Store previous questions and answers:** `qa_history` is listed in the sidebar.
3. **Preserve math context across interactions:** all earlier messages are passed to the
   agent on each new question, so follow-ups like "double that" or "now add 10%" work.
   The agent object is also stored in session state and created once per session.
   A "Clear conversation" button resets the memory.

## Notes
- Verified: tools tested directly. The agent loop and Streamlit session state (two
  questions, memory carried over) were tested with a stand-in model.
  Real-LLM answers depend on your API key and model.
- Streamlit reruns the script on each interaction, which is why session state is needed.
