"""Offline logic test: prompts, assistant functions, streaming and the Streamlit app with a fake LLM.
Run: python test_offline.py   (no Ollama needed)"""
from langchain_core.language_models.fake_chat_models import FakeListChatModel
import code_assistant as ca

# 1. every task has a template and renders system + human messages
for t in ca.TASKS:
    msgs = ca.PROMPTS[t].format_messages(**ca._variables(t, "print('hi')", "NameError"))
    assert [m.type for m in msgs] == ["system", "human"], t
    assert "```python" in msgs[0].content and "##" in msgs[0].content
print("tasks:", ca.TASKS)

# 2. the four assistant functions
llm = FakeListChatModel(responses=["## Code\nok"] * 10)
assert ca.generate_code("prime check", llm=llm).startswith("## Code")
assert ca.explain_code("x=1", llm=llm) and ca.fix_bug("1/0", "ZeroDivisionError", llm=llm) and ca.optimize_code("x", llm=llm)
assert "".join(ca.stream_task("Explain Code", "x=1", llm=llm)) == "## Code\nok"
# the debug prompt includes the error text
assert "ZeroDivisionError" in ca.PROMPTS["Debug Code"].format_messages(**ca._variables("Debug Code", "1/0", "ZeroDivisionError"))[1].content

# 3. Ollama not running is handled (no crash)
assert ca.check_ollama("http://localhost:1", "codellama:7b") == (False, False, [])

# 4. Streamlit app with a fake LLM and fake 'ollama running'
from streamlit.testing.v1 import AppTest
ca.check_ollama = lambda *a, **k: (True, True, ["codellama:7b"])
ca.get_llm = lambda *a, **k: FakeListChatModel(responses=["## Code\n```python\nprint('ok')\n```"])
at = AppTest.from_file("app.py", default_timeout=30).run()
at.selectbox[0].select("Debug Code").run()
assert len(at.text_area) == 2, "debug mode shows the error box"
at.text_area[0].input("print(1/0)").run()
at.button[0].click().run()
assert not at.exception, at.exception
assert len(at.session_state.history) == 1
print("app OK -> task:", at.session_state.history[0]["task"])
print("All offline tests passed.")
