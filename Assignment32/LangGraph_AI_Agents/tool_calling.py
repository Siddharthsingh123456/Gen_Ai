"""PART 3 - Task 6: tool binding and the tool-calling flow.

User Query -> LLM -> Tool Selection -> Tool Execution -> Final Answer

The tools are bound to the LLM with llm.bind_tools(); the LLM itself decides whether and which
tool to call. Run:  python tool_calling.py
"""
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from custom_tools import CompanyToolkit
from models import ConfigError, get_llm

SYSTEM = "You are a helpful company assistant. Use the tools when they help; never guess facts or maths."


def run_with_tools(llm, tools, query: str, max_rounds: int = 5, verbose: bool = True) -> str:
    """Executes the full tool-calling loop and returns the final answer."""
    tool_map = {t.name: t for t in tools}
    llm_with_tools = llm.bind_tools(tools)                      # Task 6, step 1: bind tools to the LLM
    messages = [SystemMessage(content=SYSTEM), HumanMessage(content=query)]
    if verbose:
        print(f"\nUSER QUERY: {query}")

    for _ in range(max_rounds):
        ai = llm_with_tools.invoke(messages)                    # LLM decides: answer or call tool(s)
        messages.append(ai)
        if not ai.tool_calls:                                   # no tool needed -> this is the answer
            if verbose:
                print("FINAL ANSWER:", ai.content)
            return ai.content
        for call in ai.tool_calls:                              # Tool Selection
            if verbose:
                print(f"  TOOL SELECTED : {call['name']}  args={call['args']}")
            try:
                result = tool_map[call["name"]].invoke(call["args"])        # Tool Execution
            except Exception as e:
                result = f"Tool error: {e}"
            if verbose:
                print(f"  TOOL RESULT   : {result}")
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return "Stopped: too many tool-calling rounds."


# Task 6: test with queries needing no tool, a single tool, and multiple tools
TEST_QUERIES = [
    "Say hello in one short sentence.",                                              # no tool
    "What is our company policy on remote work?",                                    # single tool
    "Which Engineering employees do we have and how many leave days do they have left?",  # single tool
    "Per policy, how many annual leave days do we get? If I already used 9 of them, how many remain?",  # multiple tools
    "What day is it today in Asia/Kolkata, and how much is 15% of 2480?",            # multiple tools
]

if __name__ == "__main__":
    try:
        llm = get_llm()
    except ConfigError as e:
        raise SystemExit(f"Error: {e}")
    tools = CompanyToolkit().get_tools()
    for q in TEST_QUERIES:
        run_with_tools(llm, tools, q)
