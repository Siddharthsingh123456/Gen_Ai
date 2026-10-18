"""TASK 4 - Streamlit Code Assistant app (CodeLlama via Ollama).   Run: streamlit run app.py"""
import streamlit as st
from code_assistant import HOST, MODEL, TASKS, check_ollama, get_llm, stream_task

st.set_page_config(page_title="CodeLlama Assistant", page_icon="💻", layout="wide")
st.title("💻 CodeLlama Code Assistant")
st.caption(f"Runs locally with Ollama - model: `{MODEL}`")

# ---- sidebar: Ollama status ----
running, pulled, _ = check_ollama()
with st.sidebar:
    st.header("Status")
    if not running:
        st.error(f"Ollama is not running at {HOST}. Start the Ollama app or run `ollama serve`.")
    elif not pulled:
        st.warning(f"Model not found. Run: `ollama pull {MODEL}`")
    else:
        st.success("Ollama running, model ready")
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.1)
    st.markdown("**Tips**\n- *Generate*: describe what you need\n- *Explain / Optimize*: paste code\n"
                "- *Debug*: paste code + the error message")

if "history" not in st.session_state:
    st.session_state.history = []          # previous results of this session

# ---- inputs ----
col1, col2 = st.columns([1, 2])
with col1:
    task = st.selectbox("Task type", TASKS)                      # dropdown
placeholder = {
    "Generate Code": "Describe the code you need, e.g. 'a function to check prime numbers'",
    "Explain Code": "Paste the code you want explained",
    "Debug Code": "Paste the buggy code",
    "Optimize Code": "Paste the code you want improved",
}[task]
user_input = st.text_area("Code or prompt", height=220, placeholder=placeholder)   # text area
error = ""
if task == "Debug Code":
    error = st.text_area("Error message (optional)", height=80,
                         placeholder="e.g. ZeroDivisionError: division by zero")

run = st.button(f"▶ {task}", type="primary", disabled=not user_input.strip())

# ---- output ----
if run:
    if not running:
        st.error("Cannot reach Ollama. Start it first (see sidebar).")
    elif not pulled:
        st.error(f"Pull the model first:  ollama pull {MODEL}")
    else:
        st.subheader("Result")
        try:
            llm = get_llm(temperature=temperature)
            with st.spinner("CodeLlama is thinking..."):
                result = st.write_stream(stream_task(task, user_input, error, llm=llm))   # live, readable markdown
            st.session_state.history.append({"task": task, "input": user_input, "output": result})
            st.download_button("Download answer (.md)", result, file_name="answer.md")
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")

if st.session_state.history:
    with st.expander(f"Previous results ({len(st.session_state.history)})"):
        for item in reversed(st.session_state.history):
            st.markdown(f"**{item['task']}** - `{item['input'][:60].strip()}...`")
            st.markdown(item["output"])
            st.divider()
