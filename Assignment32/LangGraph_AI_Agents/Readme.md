# GenAI Task 32 - AI Agents using LangChain

**Student:** Siddharth

An AI Assistant **Agent** that can search for information, perform calculations, query company data,
decide **which tool to use**, and explain its reasoning steps (**ReAct: Reason + Act**).
Built with LangChain + any LLM (OpenAI / Groq / Ollama). Focus is on agent logic, so there is no UI.
No fine-tuning.

## Project structure

```
GenAI-Task32-Siddharth/
├── Readme.md                  <- setup + written answers (Tasks 1, 7, 11)
├── requirements.txt
├── .env.example               <- copy to .env, choose provider + key
├── config.py / models.py      <- LLM provider (OpenAI / Groq / Ollama)
├── tools_builtin.py           <- PART 1: Task 2  (Wikipedia, web search, arXiv)
├── custom_tools.py            <- PART 2: Tasks 3-4 (custom tools + CompanyToolkit)
├── tool_calling.py            <- PART 3: Task 6  (bind_tools + tool-calling flow)
├── react_agent.py             <- PART 4: Tasks 8-9 (ReAct agent + test questions)
├── react_agent_prebuilt.py    <- bonus: same agent via LangChain's ready-made create_agent
├── agent_assistant.py         <- PART 5: Task 10 (final AI Agent Assistant)
└── test_offline.py            <- logic tests with scripted fake LLMs (no key, no internet)
```

## Task-to-file mapping

| Task | What | Where |
|------|------|-------|
| 1 | Conceptual answers | below |
| 2 | 3 built-in tools: initialise -> test -> print output | `tools_builtin.py` (`python tools_builtin.py`) |
| 3 | Custom `@tool company_policy_lookup(query: str) -> str` (mock data) + independent test | `custom_tools.py` |
| 4 | Custom toolkit grouping policy lookup, database query, date/time (+ calculator) | `custom_tools.CompanyToolkit` |
| 6 | Bind tools to LLM, LLM decides when to call; flow Query -> LLM -> Tool Selection -> Execution -> Final Answer; tests with no / single / multiple tools | `tool_calling.py` |
| 7 | ReAct overview | below |
| 8 | ReAct prompt + tools + Think / Act / Observe / Answer | `react_agent.py` |
| 9 | Test: factual (Wikipedia), calculation, multi-step; observe reasoning trace | `react_agent.py` (`TEST_QUESTIONS`) |
| 10 | Agent that answers questions, calculates, retrieves info and chooses tools itself | `agent_assistant.py` |
| 11 | Observations | below |

## Tools

| Tool | Type | Purpose |
|------|------|---------|
| `wikipedia` | built-in (`WikipediaQueryRun`) | factual questions |
| `duckduckgo_search` | built-in (`DuckDuckGoSearchRun`; uses Tavily if `TAVILY_API_KEY` is set) | current information from the web |
| `arxiv` | built-in (`ArxivQueryRun`) | research papers |
| `company_policy_lookup` | custom | leave, remote work, hours, expenses ... (mock data) |
| `employee_database_query` | custom | employees of a department from a small SQLite database (parameterised query) |
| `get_current_datetime` | custom | current date/time in a time zone |
| `calculator` | custom | safe maths evaluator (AST based - no `eval`, so no code injection) |

Note on the calculator: LangChain's old `llm-math` chain is deprecated, so the calculator is a small
custom tool. The three built-in tools are Wikipedia, web search and arXiv.

## Setup

```bash
python -m venv venv
venv\Scripts\activate           # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # macOS/Linux: cp .env.example .env   -> then add your key
```

Choose ONE provider in `.env`: **OpenAI** (`OPENAI_API_KEY`), **Groq** (`GROQ_API_KEY`, free tier) or
**Ollama** (local, no key). The web-search and Wikipedia tools need an internet connection but no key.

## Run

```bash
python tools_builtin.py          # Task 2: test the built-in tools (no LLM needed)
python custom_tools.py           # Tasks 3-4: test each custom tool independently (no LLM needed)
python tool_calling.py           # Task 6: tool binding + tool-calling flow (single & multiple tools)
python react_agent.py            # Tasks 8-9: ReAct agent with printed Thought/Action/Observation trace
python agent_assistant.py        # Task 10: interactive agent  (--demo for examples, --mode tools, --quiet)
python react_agent_prebuilt.py   # bonus: prebuilt LangChain agent
python test_offline.py           # logic tests without keys / internet
```

Example reasoning trace (ReAct):

```
QUESTION: Look up the birth year of Alan Turing on Wikipedia, then calculate how old he would be in 2026.
  Thought      : I need Turing's birth year, so I should look it up.
  Action       : wikipedia
  Action Input : Alan Turing
  Observation  : Alan Turing (born 23 June 1912) was an English mathematician ...
  Thought      : Born in 1912. Age in 2026 = 2026 - 1912. I should use the calculator.
  Action       : calculator
  Action Input : 2026 - 1912
  Observation  : 114
  Final Answer : Alan Turing would be 114 years old in 2026.
```

## How the agent works

**Tool calling (Task 6):** `llm.bind_tools(tools)` sends the tool descriptions to the model. The model returns
either a normal answer or a *tool call* (name + arguments). The program runs the tool, sends the result back
as a `ToolMessage`, and the model writes the final answer (looping if more tools are needed).

**ReAct (Task 8):** the prompt describes the tools and the format `Thought / Action / Action Input / Observation /
Final Answer`. The LLM is stopped before it writes "Observation:", the program runs the chosen tool, appends the
real result as the observation, and calls the LLM again - until it writes a Final Answer. The loop is written out
explicitly (equivalent to LangChain's `create_react_agent`) so every step can be seen and printed. Safety features:
step limit (no infinite loops), invalid tool names and tool errors are returned to the model as observations so it can
recover, and a graceful fallback if the model ignores the format.

## Task 1 - Understanding Tools (conceptual)

**1. What is a tool in an AI agent?**
A tool is a function the agent can call to do something the LLM cannot do by itself - search the web, do exact
maths, query a database, read a file or call an API. It has a name, a description (which the LLM reads to decide
when to use it) and defined inputs/outputs.

**2. Why do agents need tools?**
An LLM only knows its training data, cannot access private or live information, is unreliable at exact
arithmetic, and cannot take actions in the world. Tools give it fresh facts, accuracy and the ability to act,
which also reduces hallucination because answers come from real tool outputs.

**3. Difference between a chatbot and an agent**
A chatbot takes a message and produces a text reply from the model's knowledge (optionally with fixed retrieval).
An agent works towards a goal: it reasons about what to do, chooses and calls tools, observes the results, and
repeats until the task is done. The agent decides the steps at run time; a chatbot follows one fixed step.

## Task 7 - ReAct Agent Overview (conceptual)

**1. What is ReAct (Reason + Act)?**
ReAct is a pattern where the LLM alternates between **reasoning** (a written *Thought* about what to do next)
and **acting** (calling a tool with an *Action*), then reads the *Observation* (tool result) and reasons again,
until it can give a *Final Answer*.

**2. Why are ReAct agents powerful?**
They can solve multi-step problems (look up -> calculate -> compare), correct themselves when a tool returns
something unexpected, ground answers in real tool output instead of guessing, and their visible reasoning trace
makes behaviour easy to debug and explain.

## Task 11 - Observations & Insights

**1. Benefits of tool-augmented agents**
Access to up-to-date and private information, exact calculations, ability to take actions, fewer
hallucinations (answers are backed by tool output), modular design (add a capability by adding a tool), and
transparent reasoning steps.

**2. Challenges with agents**
Wrong tool choice or bad tool input; looping or wandering without progress; higher latency and token cost
(several LLM calls per question); non-deterministic behaviour that is harder to test; format errors with
weaker models; and safety risks if tools are powerful (code execution, SQL, file access), so tools must be
validated - here the calculator avoids `eval` and the database tool uses parameterised queries.

**3. Difference between chains and agents**
A chain is a fixed sequence of steps decided by the developer (e.g. retrieve -> prompt -> LLM). An agent lets the
LLM decide at run time which steps and tools to use and how many times. Chains are predictable, cheaper and faster;
agents are flexible but less predictable.

**4. When to use agents over RAG**
Use plain RAG when the task is "answer from a known document collection" - it is simpler, cheaper and more
predictable. Use an agent when the question needs *several* sources or capabilities (documents + database +
calculator + web), multi-step reasoning, live data, or real actions. An agent can even use RAG as one of its tools.

## Notes

- API keys are read from `.env` (not included in the zip); nothing is hard-coded.
- Built-in tools need internet access. If Wikipedia / web search / arXiv are unreachable, the tool returns an error as
  an observation and the agent continues with the other tools.
- Package note: LangChain's DuckDuckGo wrapper needs the `ddgs` package, and its arXiv wrapper needs `arxiv<3`
  (both already set in `requirements.txt`).
