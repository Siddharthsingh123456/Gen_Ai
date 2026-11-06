"""Offline logic test (no model download): checks the chains/templates with a fake LLM.
Run: python test_logic.py"""
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = FakeListLLM(responses=["Canberra", "Shakespeare"])
chain = PromptTemplate.from_template("Answer the question: {question}") | llm | StrOutputParser()
assert chain.invoke({"question": "capital of Australia?"}) == "Canberra"
assert chain.invoke({"question": "who wrote Romeo and Juliet?"}) == "Shakespeare"

chat_prompt = ChatPromptTemplate.from_messages([("system", "You are a {role}."), ("human", "{question}")])
msgs = chat_prompt.format_messages(role="pirate", question="Hi?")
assert [m.type for m in msgs] == ["system", "human"]
out = (chat_prompt | FakeListChatModel(responses=["Arr!"]) | StrOutputParser()).invoke({"role": "pirate", "question": "Hi?"})
assert out == "Arr!"
print("All logic tests passed.")
