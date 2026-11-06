"""BONUS - the same idea with LangChain's ready-made agent (no hand-written loop).

LangChain >= 1.0 : langchain.agents.create_agent
LangChain 0.3    : langgraph.prebuilt.create_react_agent   (pip install langgraph)

Run:  python react_agent_prebuilt.py "How old would Alan Turing be in 2026?"
"""
import sys

from custom_tools import CompanyToolkit
from models import ConfigError, get_llm
from tools_builtin import get_builtin_tools

SYSTEM_PROMPT = ("You are a helpful assistant. Think step by step, use the tools for facts, company "
                 "information and any arithmetic, and explain briefly how you got the answer.")


def build_prebuilt_agent(llm, tools):
    try:
        from langchain.agents import create_agent                       # LangChain >= 1.0
        return create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)
    except ImportError:
        from langgraph.prebuilt import create_react_agent               # LangChain 0.3 + langgraph
        return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)


def run(agent, question: str) -> str:
    result = agent.invoke({"messages": [("user", question)]})
    for m in result["messages"]:                                        # print the reasoning trace
        if m.type == "ai" and getattr(m, "tool_calls", None):
            for c in m.tool_calls:
                print(f"  ACT         : {c['name']}({c['args']})")
        elif m.type == "tool":
            print(f"  OBSERVATION : {str(m.content)[:300]}")
    answer = result["messages"][-1].content
    print("  ANSWER      :", answer)
    return answer


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Who created Python, and how many years ago was that if the year is 2026?"
    try:
        agent = build_prebuilt_agent(get_llm(), get_builtin_tools() + CompanyToolkit().get_tools())
    except ConfigError as e:
        raise SystemExit(f"Error: {e}")
    run(agent, question)
