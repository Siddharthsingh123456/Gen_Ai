"""TASK 1 - verify that Ollama is running and CodeLlama is pulled.

Setup commands (run in a terminal):
    1. Install Ollama:  https://ollama.com/download   (Windows / macOS installer, Linux: curl -fsSL https://ollama.com/install.sh | sh)
    2. ollama pull codellama:7b
    3. ollama list            # codellama:7b should appear
       ollama run codellama:7b "Say hello"   # quick manual test
"""
from code_assistant import HOST, MODEL, check_ollama

running, pulled, models = check_ollama()
print(f"Ollama server ({HOST}): {'RUNNING' if running else 'NOT RUNNING'}")
if not running:
    print("-> Start it with `ollama serve` (or open the Ollama app), then run this script again.")
    raise SystemExit(1)
print("Installed models:", models or "none")
print(f"Model {MODEL}: {'READY' if pulled else 'NOT PULLED -> run: ollama pull ' + MODEL}")
if pulled:
    import ollama
    reply = ollama.chat(model=MODEL, messages=[{"role": "user", "content": "Reply with the single word: ready"}])
    print("Test response:", reply["message"]["content"].strip())
    print("\nSetup verified.")
