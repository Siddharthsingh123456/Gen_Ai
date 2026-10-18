"""TASK 2 - Basic CodeLlama interaction: (a) Ollama Python library, (b) LangChain wrapper."""
import ollama
from langchain_ollama import ChatOllama
from code_assistant import HOST, MODEL

SAMPLE_CODE = """def f(n):
    r = []
    for i in range(n):
        if i % 2 == 0:
            r.append(i * i)
    return r
"""

PROMPTS = [
    "Write a Python function to check prime numbers",
    f"Explain this code:\n{SAMPLE_CODE}",
]

print(f"Model: {MODEL}\n")

print("########## (a) Ollama Python library ##########")
client = ollama.Client(host=HOST)
for p in PROMPTS:
    print(f"\n>>> {p}\n")
    reply = client.chat(model=MODEL, messages=[{"role": "user", "content": p}])
    print(reply["message"]["content"])

print("\n\n########## (b) LangChain wrapper (ChatOllama) ##########")
llm = ChatOllama(model=MODEL, base_url=HOST, temperature=0.2)
for p in PROMPTS:
    print(f"\n>>> {p}\n")
    print(llm.invoke(p).content)
