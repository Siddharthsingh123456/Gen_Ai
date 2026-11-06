"""GenAI Assistant - a small chat app built for deployment on Streamlit Cloud and Hugging Face Spaces.
Run locally:  streamlit run app.py"""
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from llm_factory import PROVIDERS, get_llm, get_secret

st.set_page_config(page_title="GenAI Assistant", page_icon="🤖")
st.title("🤖 GenAI Assistant")
st.caption("A deployable GenAI app: Streamlit + LangChain + Groq/OpenAI")

PERSONAS = {
    "General assistant": "You are a helpful, concise assistant.",
    "Study tutor": "You are a friendly tutor. Explain step by step with simple examples.",
    "Code helper": "You are a senior Python developer. Give short, correct code with brief explanations.",
    "Summarizer": "You summarize any text the user sends into 3-5 clear bullet points.",
}

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Model provider", list(PROVIDERS))
    cfg = PROVIDERS[provider]
    model = st.text_input("Model", cfg["default_model"])
    persona = st.selectbox("Assistant mode", list(PERSONAS))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

    server_key = get_secret(cfg["key_name"])
    user_key = ""
    if not server_key:
        user_key = st.text_input(f"{cfg['key_name']}", type="password",
                                 help="Not stored. Used only for this session.")
    api_key = server_key or user_key
    st.success("API key found" if api_key else "No API key yet")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
    st.caption("On a deployed app the key comes from the platform's *Secrets* settings.")

# ---------------- session state ----------------
st.session_state.setdefault("messages", [])          # [{"role": "user"|"assistant", "content": str}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- chat ----------------
prompt = st.chat_input("Ask me anything...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    if not api_key:
        st.warning(f"Add `{cfg['key_name']}` in the app's Secrets (or paste it in the sidebar) to start chatting.")
        st.stop()

    history = [SystemMessage(content=PERSONAS[persona])]
    for m in st.session_state.messages:
        history.append(HumanMessage(content=m["content"]) if m["role"] == "user"
                       else AIMessage(content=m["content"]))
    history.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        try:
            llm = get_llm(provider, model, temperature, api_key)
            reply = st.write_stream(chunk.content for chunk in llm.stream(history))
        except Exception as exc:
            reply = f"Sorry, the model call failed: `{type(exc).__name__}`. Check the API key, model name and quota."
            st.error(reply)
    st.session_state.messages += [{"role": "user", "content": prompt},
                                  {"role": "assistant", "content": reply}]
