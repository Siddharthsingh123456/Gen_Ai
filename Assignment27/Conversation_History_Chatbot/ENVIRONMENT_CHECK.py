import importlib.util

packages = [
    "langchain",
    "langchain_core",
    "langchain_ollama",
    "streamlit",
    "dotenv"
]

print("Package check")
print("-" * 30)

for package in packages:
    if importlib.util.find_spec(package):
        print(package, "OK")
    else:
        print(package, "MISSING")

print("\nNext check Ollama manually with:")
print("ollama --version")
print("ollama list")
