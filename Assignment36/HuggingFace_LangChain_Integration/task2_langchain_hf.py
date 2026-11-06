"""TASK 2 - HuggingFace with LangChain.

1. Integrate the HuggingFace model using the LangChain wrapper (HuggingFacePipeline)
2. Replace OpenAI in an LLM chain with HuggingFace
3. Test with multiple prompts
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from hf_utils import get_text_llm, TEXT_MODEL, HF_MODE

# ---------------------------------------------------------------------------------
# BEFORE (closed API):
#     from langchain_openai import ChatOpenAI
#     llm = ChatOpenAI(model="gpt-4o-mini")
# AFTER (open-source HuggingFace model, only this one line changes):
llm = get_text_llm()
# ---------------------------------------------------------------------------------
print(f"LLM backend: HuggingFace ({HF_MODE}) | model: {TEXT_MODEL}\n")

# Same chain structure as with OpenAI:  prompt | llm | output parser
prompt = PromptTemplate.from_template("Answer the question: {question}")
chain = prompt | llm | StrOutputParser()

questions = [
    "What is the capital of Australia?",
    "Who wrote the play Romeo and Juliet?",
    "What is 12 multiplied by 8?",
    "Name one renewable energy source.",
    "What is the opposite of 'expensive'?",
]
print("=== Test 1: question answering chain ===")
for q in questions:
    print(f"Q: {q}\nA: {chain.invoke({'question': q})}\n")

# A second chain with a different prompt template (translation + summarization)
translate = PromptTemplate.from_template("Translate English to {language}: {text}") | llm | StrOutputParser()
summarize = PromptTemplate.from_template("Summarize: {text}") | llm | StrOutputParser()

print("=== Test 2: translation chain ===")
for lang in ["French", "German", "Romanian"]:
    print(f"{lang}: {translate.invoke({'language': lang, 'text': 'Good morning, my friend.'})}")

print("\n=== Test 3: summarization chain ===")
text = ("LangChain is a framework for building applications with language models. It provides "
        "prompt templates, chains, memory and integrations with many model providers, including "
        "HuggingFace, so developers can swap models without rewriting their application.")
print(summarize.invoke({"text": text}))

print("\n=== Test 4: batch of prompts ===")
for ans in chain.batch([{"question": q} for q in questions[:3]]):
    print("-", ans)
