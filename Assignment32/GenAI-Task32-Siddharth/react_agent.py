"""PART 4 - Tasks 7, 8, 9: a ReAct (Reason + Act) agent.

ReAct = the LLM repeats   Thought -> Action -> Observation   until it can give a Final Answer:

    Question:  ...
    Thought:   I need the birth year of Alan Turing, so I should look it up.
    Action:    wikipedia
    Action Input: Alan Turing
    Observation: (tool output, inserted by the program)
    Thought:   I now know the birth year. I should calculate his age with the calculator.
    ...
    Final Answer: ...

The loop is written out explicitly (instead of hiding it in a library call) so that every
Think / Act / Observe / Answer step is visible. It works with any chat model (OpenAI, Groq, Ollama).

Run:  python react_agent.py          (runs the Task 9 test questions and prints the reasoning trace)
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional

from langchain_core.prompts import PromptTemplate

import config
from custom_tools import CompanyToolkit
from models import ConfigError, get_llm
from tools_builtin import get_builtin_tools

# ----------------------------------------------------------------- Task 8, step 1: ReAct prompt
REACT_TEMPLATE = """Answer the following question as best you can. You have access to these tools:

{tools}

Use EXACTLY this format:

Question: the input question you must answer
Thought: think about what to do next
Action: the tool to use, must be one of [{tool_names}]
Action Input: the input for the tool, on a single line
Observation: the result of the action (it is filled in for you - never write it yourself)
... (this Thought / Action / Action Input / Observation cycle can repeat several times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Rules:
- Use a tool whenever you need facts, company information, the date, or ANY arithmetic.
- Write only ONE Action at a time, then stop and wait for the Observation.
- If no tool is needed, go straight to "Thought: I now know the final answer".

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

REACT_PROMPT = PromptTemplate.from_template(REACT_TEMPLATE)

ACTION_RE = re.compile(r"Action\s*:\s*(.+?)\s*\n\s*Action\s*Input\s*:\s*(.*)", re.DOTALL | re.IGNORECASE)
FINAL_RE = re.compile(r"Final\s*Answer\s*:\s*(.*)", re.DOTALL | re.IGNORECASE)


@dataclass
class Step:
    thought: str
    action: Optional[str] = None
    action_input: Optional[str] = None
    observation: Optional[str] = None


@dataclass
class AgentResult:
    answer: str
    steps: List[Step] = field(default_factory=list)


def _clean(text: str) -> str:
    return text.strip().strip("`").strip().strip("\"'").strip()


class ReActAgent:
    """Task 8: ReAct agent = ReAct prompt + tools + the Think/Act/Observe/Answer loop."""

    def __init__(self, llm, tools, max_steps: int = config.MAX_AGENT_STEPS, verbose: bool = True):
        self.tools = {t.name: t for t in tools}                       # Task 8, step 2: attach tools
        self.llm = llm.bind(stop=["\nObservation:", "\nObservation :"])   # LLM must stop before "Observation:"
        self.max_steps = max_steps
        self.verbose = verbose
        self.tool_text = "\n".join(f"{t.name}: {t.description}" for t in tools)
        self.tool_names = ", ".join(self.tools)

    def _log(self, label: str, text: str) -> None:
        if self.verbose:
            print(f"  {label:<13}: {text}")

    def _call_llm(self, question: str, scratchpad: str) -> str:
        prompt = REACT_PROMPT.format(tools=self.tool_text, tool_names=self.tool_names,
                                     input=question, agent_scratchpad=scratchpad)
        out = self.llm.invoke(prompt)
        text = out.content if hasattr(out, "content") else str(out)
        return text.split("\nObservation:")[0]                        # safety: drop hallucinated observations

    def run(self, question: str) -> AgentResult:
        if self.verbose:
            print(f"\nQUESTION: {question}")
        scratchpad, steps, format_errors = "", [], 0

        for _ in range(self.max_steps):
            text = self._call_llm(question, scratchpad)
            action = ACTION_RE.search(text)

            if action:                                                # ---- THINK -> ACT
                thought = text[: action.start()].strip()
                name = _clean(action.group(1))
                tool_input = _clean(action.group(2).splitlines()[0] if action.group(2).strip() else "")
                self._log("Thought", thought)
                self._log("Action", name)
                self._log("Action Input", tool_input)
                if name not in self.tools:
                    observation = f"'{name}' is not a valid tool. Use one of: {self.tool_names}"
                else:
                    try:
                        observation = str(self.tools[name].invoke(tool_input))   # ---- OBSERVE
                    except Exception as e:
                        observation = f"Tool error: {e}"
                observation = observation[:1500]
                self._log("Observation", observation.replace("\n", " ")[:300])
                steps.append(Step(thought, name, tool_input, observation))
                scratchpad += f"{text.strip()}\nObservation: {observation}\nThought:"
                continue

            final = FINAL_RE.search(text)
            if final:                                                 # ---- ANSWER
                thought = text[: final.start()].strip()
                answer = final.group(1).strip()
                if thought:
                    self._log("Thought", thought)
                    steps.append(Step(thought))
                self._log("Final Answer", answer)
                return AgentResult(answer, steps)

            format_errors += 1                                        # model ignored the format
            if format_errors >= 2:
                self._log("Final Answer", text.strip())
                return AgentResult(text.strip(), steps)
            scratchpad += (f"{text.strip()}\nObservation: Invalid format. Reply with "
                           f"'Action:' and 'Action Input:' or with 'Final Answer:'.\nThought:")

        return AgentResult("I could not finish within the step limit.", steps)


# ----------------------------------------------------------------- Task 9: test questions
TEST_QUESTIONS = [
    ("Factual (Wikipedia)",       "Who created the Python programming language, and in which year was it first released?"),
    ("Calculation",               "What is ((1234 * 56) + 789) / 3 ?"),
    ("Multi-step reasoning",      "Look up the birth year of Alan Turing on Wikipedia, then calculate how old he would be in 2026."),
    ("Multi-step (company data)", "How many annual leave days does the company policy give, and how many has Rohan Mehta already used if he has 9 left?"),
]


def build_default_agent(verbose: bool = True) -> ReActAgent:
    tools = get_builtin_tools() + CompanyToolkit().get_tools()
    return ReActAgent(get_llm(), tools, verbose=verbose)


if __name__ == "__main__":
    try:
        agent = build_default_agent()
    except ConfigError as e:
        raise SystemExit(f"Error: {e}")
    for label, question in TEST_QUESTIONS:
        print(f"\n{'=' * 70}\nTEST: {label}")
        result = agent.run(question)
        print(f"  -> {len(result.steps)} reasoning step(s)")
