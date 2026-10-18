"""TASK 1 - Getting started with HuggingFace models (plain `transformers`, no LangChain yet).

1. Load a HuggingFace model (google/flan-t5-base)
2. Generate a response for a simple prompt
3. Observe output quality on several kinds of prompts
"""
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from hf_utils import TEXT_MODEL, TOKEN

print(f"Loading model: {TEXT_MODEL} ...")
start = time.time()
tokenizer = AutoTokenizer.from_pretrained(TEXT_MODEL, token=TOKEN)
model = AutoModelForSeq2SeqLM.from_pretrained(TEXT_MODEL, token=TOKEN)
print(f"Loaded in {time.time() - start:.1f}s | parameters: {model.num_parameters() / 1e6:.0f}M")

# --- Step 2: generate a response to a simple prompt (low-level API) ---
prompt = "Translate English to French: How are you today?"
inputs = tokenizer(prompt, return_tensors="pt")
output_ids = model.generate(**inputs, max_new_tokens=50)
print("\n=== Simple prompt ===")
print("Prompt  :", prompt)
print("Response:", tokenizer.decode(output_ids[0], skip_special_tokens=True))

# --- Step 3: observe output quality using the high-level pipeline ---
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
tests = {
    "Translation": "Translate English to German: The weather is nice today.",
    "Question answering": "Answer the question: What is the capital of Japan?",
    "Summarization": ("Summarize: Solar and wind power have become much cheaper over the last decade, "
                      "which is why many countries are building more renewable energy plants and "
                      "batteries to store the electricity."),
    "Reasoning": "Answer the question: If a train travels 60 km in 1 hour, how far does it go in 3 hours?",
    "Open-ended / creative": "Write a short poem about the ocean.",
    "Sentiment": "Is this review positive or negative? 'The food was cold and the service was slow.'",
}
print("\n=== Output quality observations ===")
for name, text in tests.items():
    t0 = time.time()
    out = generator(text, max_new_tokens=80)[0]["generated_text"]
    print(f"\n[{name}] ({time.time() - t0:.1f}s)\n  Prompt  : {text}\n  Response: {out}")

print("""
Observations (flan-t5-base):
- Good at short, instruction-style tasks: translation, factual Q&A, sentiment, short summaries.
- Answers are short; it is not a chatty assistant and ignores long-form requests.
- Weak at multi-step reasoning and creative writing (often one line or repetitive).
- Small, fast, free and runs on CPU, but less capable than large closed models.
""")
