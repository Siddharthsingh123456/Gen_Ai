"""PART 5 - Task 10: the AI Agent Assistant (mini project).

An assistant that
  * answers questions        (Wikipedia, web search, arXiv)
  * performs calculations    (calculator)
  * retrieves information    (company policy lookup, employee database, date/time)
and automatically chooses which tool to use, explaining its reasoning steps.

Run:  python agent_assistant.py                 interactive ReAct agent (shows Thought/Action/Observation)
      python agent_assistant.py --demo          runs a few example questions
      python agent_assistant.py --mode tools    uses native tool calling (bind_tools) instead of ReAct text
"""
import argparse

from custom_tools import CompanyToolkit
from models import ConfigError, get_llm
from react_agent import ReActAgent
from tool_calling import run_with_tools
from tools_builtin import get_builtin_tools

DEMO = [
    "What is our remote work policy?",
    "What is 18% of 2450, plus 120?",
    "Who is the HR team and how many leave days does each person have left?",
    "Who wrote the paper 'Attention Is All You Need'? Use arXiv or Wikipedia.",
    "Tell me a fun fact about the Moon (use Wikipedia), then tell me today's date.",
]


def main():
    ap = argparse.ArgumentParser(description="AI Agent Assistant")
    ap.add_argument("--mode", choices=["react", "tools"], default="react")
    ap.add_argument("--demo", action="store_true", help="run example questions and exit")
    ap.add_argument("--quiet", action="store_true", help="hide the reasoning trace")
    args = ap.parse_args()

    try:
        llm = get_llm()
    except ConfigError as e:
        raise SystemExit(f"Error: {e}")
    tools = get_builtin_tools() + CompanyToolkit().get_tools()

    if args.mode == "react":
        agent = ReActAgent(llm, tools, verbose=not args.quiet)
        ask = lambda q: agent.run(q).answer
    else:
        ask = lambda q: run_with_tools(llm, tools, q, verbose=not args.quiet)

    print(f"AI Agent Assistant ({args.mode} mode). Tools: {[t.name for t in tools]}")
    if args.demo:
        for q in DEMO:
            ask(q)
        return
    print("Ask anything. Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break
        try:
            answer = ask(q)
        except Exception as e:                      # network, rate limit, ...
            answer = f"Sorry, something went wrong: {e}"
        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    main()
