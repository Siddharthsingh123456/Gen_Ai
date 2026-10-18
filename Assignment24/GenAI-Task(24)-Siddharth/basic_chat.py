"""Task 1 (steps 3-5): Send a simple prompt to a local Ollama model via
LangChain's Ollama wrapper and print the response. Traced by LangSmith."""
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()  # loads LANGSMITH_* variables -> tracing turns on automatically

MODEL = os.getenv("OLLAMA_MODEL", "llama3")

llm = ChatOllama(model=MODEL, temperature=0.7)

prompt = "Explain what a Large Language Model is in two sentences."
response = llm.invoke(prompt)

print(f"Model  : {MODEL}")
print(f"Prompt : {prompt}")
print(f"Answer : {response.content}")
