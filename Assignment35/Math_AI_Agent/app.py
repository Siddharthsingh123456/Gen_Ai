"""Streamlit app: Text-to-Math Problem Solver with session state.   Run: streamlit run app.py"""
import streamlit as st
from math_agent import build_agent, solve

st.set_page_config(page_title="Text-to-Math Agent", page_icon="🧮")
st.title("🧮 Text-to-Math Problem Solver")
st.caption("Ask a word problem, a percentage question or simple algebra. The agent solves it step by step.")

# ---------------- Session state (Task 3) ----------------
if "messages" not in st.session_state:       # 1. conversation history (shown + sent to the agent)
    st.session_state.messages = []
if "qa_history" not in st.session_state:     # 2. stored previous questions & answers
    st.session_state.qa_history = []
if "agent" not in st.session_state:          # agent created once per session
    try:
        st.session_state.agent = build_agent()
    except Exception as exc:
        st.session_state.agent = None
        st.error(f"Could not start the agent: {exc}\n\nCheck your .env file (LLM_PROVIDER / API key).")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Session memory")
    st.write(f"Questions asked: **{len(st.session_state.qa_history)}**")
    for i, qa in enumerate(st.session_state.qa_history, 1):
        st.markdown(f"**{i}.** {qa['question']}")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.qa_history = []
        st.rerun()
    st.divider()
    st.markdown("**Try:**\n- What is 15% of 240?\n- A shirt costs $80 with 25% off. What is the sale price?\n"
                "- Solve 3x + 7 = 25\n- Now multiply that answer by 4  *(uses memory)*")

# ---------------- Show history ----------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("steps"):
            with st.expander("Tool calls"):
                for s in m["steps"]:
                    st.code(f"{s['tool']}({s['input']})  ->  {s['output']}")

# ---------------- New question ----------------
question = st.chat_input("Type a math problem...")
if question and st.session_state.agent:
    with st.chat_message("user"):
        st.markdown(question)
    # 3. math context is preserved: previous turns are passed to the agent
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    with st.chat_message("assistant"):
        with st.spinner("Solving..."):
            try:
                answer, steps = solve(st.session_state.agent, question, history)
            except Exception as exc:
                answer, steps = f"Sorry, something went wrong: {exc}", []
        st.markdown(answer)
        if steps:
            with st.expander("Tool calls"):
                for s in steps:
                    st.code(f"{s['tool']}({s['input']})  ->  {s['output']}")
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer, "steps": steps})
    st.session_state.qa_history.append({"question": question, "answer": answer})
    st.rerun()
