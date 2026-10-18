"""Offline logic test - NO API key, NO internet.   Run: python test_offline.py

Checks the custom tools for real, and the tool-calling flow + ReAct loop with scripted fake LLMs.
"""
from langchain_core.language_models.fake_chat_models import FakeListChatModel, FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from custom_tools import (CompanyToolkit, calculator, company_policy_lookup,
                          employee_database_query, get_current_datetime)
from react_agent import ReActAgent
from tool_calling import run_with_tools

# ------------------------------------------------------------------ custom tools (Tasks 3-4)
assert "24 days" in company_policy_lookup.invoke("leave")
assert "No policy found" in company_policy_lookup.invoke("stock options")
assert "Asha Verma" in employee_database_query.invoke("engineering")
assert "No employees" in employee_database_query.invoke("Marketing")
assert employee_database_query.invoke("'; DROP TABLE employees; --").startswith("No employees found")
assert "Kabir Singh" in employee_database_query.invoke("HR")      # table still intact after injection attempt
assert calculator.invoke("(24 - 10) * 3 + 2**5") == "74"
assert calculator.invoke("10 / 4") == "2.5"
assert calculator.invoke("10 / 0").startswith("Error")
assert calculator.invoke("__import__('os').system('ls')").startswith("Error")   # code injection blocked
assert "UTC" in get_current_datetime.invoke("nonsense/zone")
assert len(CompanyToolkit().get_tools()) == 4
print("[ok] custom tools + toolkit work (incl. SQL / code-injection safety)")

# ------------------------------------------------------------------ tool calling flow (Task 6)
class FakeToolModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

def call(name, args, cid):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": cid}])

tools = CompanyToolkit().get_tools()
llm = FakeToolModel(responses=[
    call("company_policy_lookup", {"query": "leave"}, "c1"),
    AIMessage(content="", tool_calls=[{"name": "calculator", "args": {"expression": "24 - 9"}, "id": "c2"}]),
    AIMessage(content="You get 24 days; after using 9 you have 15 left."),
])
answer = run_with_tools(llm, tools, "How many leave days remain after using 9?", verbose=False)
assert "15" in answer
llm = FakeToolModel(responses=[AIMessage(content="Hello!")])
assert run_with_tools(llm, tools, "hi", verbose=False) == "Hello!"          # no tool needed
print("[ok] tool-calling loop: multiple tools in sequence, and no-tool answer")

# ------------------------------------------------------------------ ReAct loop (Tasks 8-9)
@tool("wikipedia")
def fake_wikipedia(query: str) -> str:
    """Fake Wikipedia for the offline test."""
    return "Alan Turing (born 23 June 1912) was an English mathematician."

react_tools = [fake_wikipedia, calculator]
llm = FakeListChatModel(responses=[
    " I need Turing's birth year.\nAction: wikipedia\nAction Input: Alan Turing",
    " Born in 1912. Age in 2026 = 2026 - 1912.\nAction: calculator\nAction Input: 2026 - 1912",
    " I now know the final answer\nFinal Answer: Alan Turing would be 114 years old in 2026.",
])
res = ReActAgent(llm, react_tools, verbose=False).run("How old would Alan Turing be in 2026?")
assert "114" in res.answer
assert [s.action for s in res.steps if s.action] == ["wikipedia", "calculator"]
assert "1912" in res.steps[0].observation and res.steps[1].observation == "114"
print("[ok] ReAct: Think -> Act -> Observe (x2) -> Answer; trace recorded:",
      [(s.action, s.action_input) for s in res.steps if s.action])

llm = FakeListChatModel(responses=[
    " Try something.\nAction: magic_tool\nAction Input: x",
    " Use the calculator.\nAction: calculator\nAction Input: 6 * 7",
    " I now know the final answer\nFinal Answer: 42",
])
res = ReActAgent(llm, react_tools, verbose=False).run("6 times 7?")
assert res.answer == "42" and "not a valid tool" in res.steps[0].observation
print("[ok] ReAct recovers from an invalid tool name")

llm = FakeListChatModel(responses=["I just answer in free text.", "Still free text."])
res = ReActAgent(llm, react_tools, verbose=False).run("anything")
assert res.answer == "Still free text."
print("[ok] ReAct falls back gracefully when the model ignores the format")

llm = FakeListChatModel(responses=[" Loop.\nAction: calculator\nAction Input: 1+1"])
res = ReActAgent(llm, react_tools, max_steps=3, verbose=False).run("loop forever")
assert "step limit" in res.answer
print("[ok] ReAct stops at the step limit (no infinite loop)")

# ------------------------------------------------------------------ bonus prebuilt agent
try:
    from react_agent_prebuilt import build_prebuilt_agent
    llm = FakeToolModel(responses=[call("calculator", {"expression": "2*21"}, "p1"), AIMessage(content="The answer is 42.")])
    out = build_prebuilt_agent(llm, [calculator]).invoke({"messages": [("user", "2*21?")]})
    assert out["messages"][-1].content == "The answer is 42."
    print("[ok] bonus prebuilt agent runs (create_agent / create_react_agent)")
except ImportError:
    print("[skip] prebuilt agent needs langchain>=1.0 or langgraph")

print("\nAll offline checks passed.")
