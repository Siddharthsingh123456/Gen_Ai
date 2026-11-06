"""Offline test of the app (no API key / network needed). Run: python test_offline.py"""
from langchain_core.language_models.fake_chat_models import FakeListChatModel
import llm_factory
from streamlit.testing.v1 import AppTest

# 1. No key: the app loads and warns instead of crashing
at = AppTest.from_file("app.py", default_timeout=30).run()
assert not at.exception
at.chat_input[0].set_value("hello").run()
assert not at.exception and any("Secrets" in w.value for w in at.warning), "should ask for a key"
print("no-key behaviour OK")

# 2. With a key (pasted in the sidebar) and a fake model: streaming reply + session memory
fake = FakeListChatModel(responses=["Hi! I am fake.", "Second reply."])
llm_factory.get_llm = lambda *a, **k: fake
at = AppTest.from_file("app.py", default_timeout=30).run()
at.sidebar.text_input[1].set_value("test-key").run()      # [0]=model, [1]=API key
at.chat_input[0].set_value("hello").run()
at.chat_input[0].set_value("again").run()
assert not at.exception, at.exception
assert [m["content"] for m in at.session_state.messages if m["role"] == "assistant"] == ["Hi! I am fake.", "Second reply."]
print("chat + session state OK ->", len(at.session_state.messages), "messages")
print("All offline tests passed.")
