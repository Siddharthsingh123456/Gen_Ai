"""Text-to-Math agent: LangChain agent + LLM + math tools, with conversation memory."""
import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from math_tools import TOOLS

load_dotenv()

SYSTEM_PROMPT = """You are a careful Text-to-Math assistant that solves math problems step by step.

Follow this process:
1. Understand the problem (word problem, arithmetic, percentage, or simple algebra).
2. Break it into small steps and say what each step does.
3. NEVER calculate in your head: use the `calculator` tool for every arithmetic operation
   and the `solve_equation` tool for algebra equations.
4. Use earlier messages in the conversation when the user refers to them
   ("that result", "the previous answer", "now double it").
5. Finish with a line exactly like:  Final Answer: <result with units if relevant>
If the problem is not a math problem or is missing information, ask a short clarifying question."""


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), temperature=0)
    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.1"), temperature=0)
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")


def build_agent(llm=None):
    """Create the tool-calling agent (works with LangChain 1.x, falls back to LangGraph)."""
    llm = llm or get_llm()
    try:
        from langchain.agents import create_agent
        return create_agent(llm, TOOLS, system_prompt=SYSTEM_PROMPT)
    except ImportError:
        from langgraph.prebuilt import create_react_agent
        return create_react_agent(llm, TOOLS, prompt=SYSTEM_PROMPT)


def to_lc_messages(history):
    """Convert [{'role': 'user'|'assistant', 'content': str}, ...] to LangChain messages."""
    msgs = []
    for m in history:
        cls = HumanMessage if m["role"] == "user" else AIMessage
        msgs.append(cls(content=m["content"]))
    return msgs


def _text(content):
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return content or ""


def solve(agent, question: str, history=None):
    """Run the agent. `history` = previous Q&A messages (session memory).
    Returns (answer_text, steps) where steps lists every tool call made."""
    messages = to_lc_messages(history or []) + [HumanMessage(content=question)]
    result = agent.invoke({"messages": messages})
    out = result["messages"][len(messages):]          # only the new messages of this turn

    steps, pending = [], {}
    for m in out:
        if isinstance(m, AIMessage):
            for call in m.tool_calls:
                pending[call["id"]] = {"tool": call["name"], "input": call["args"], "output": None}
                steps.append(pending[call["id"]])
        elif isinstance(m, ToolMessage) and m.tool_call_id in pending:
            pending[m.tool_call_id]["output"] = _text(m.content)
    answer = _text(out[-1].content) if out else ""
    return answer, steps


if __name__ == "__main__":
    agent = build_agent()
    chat = []
    print("Text-to-Math agent (type 'exit' to quit)")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        ans, steps = solve(agent, q, chat)
        for s in steps:
            print(f"  [tool] {s['tool']}({s['input']}) -> {s['output']}")
        print("Agent:", ans)
        chat += [{"role": "user", "content": q}, {"role": "assistant", "content": ans}]
