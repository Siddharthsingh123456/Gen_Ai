"""TASK 3 - ChatPromptTemplate with HuggingFace.

1. Create a ChatPromptTemplate
2. Use system + human messages
3. Generate responses with a HuggingFace-backed LLM (ChatHuggingFace)
4. Compare with a normal prompt template
"""
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from hf_utils import get_causal_llm, get_chat_model, CHAT_MODEL, HF_MODE

print(f"Chat model: {CHAT_MODEL} ({HF_MODE})\n")
base_llm = get_causal_llm()            # raw text-generation LLM (string in -> string out)
chat_model = get_chat_model(base_llm)  # same weights, wrapped to accept chat messages

# ---- Steps 1 & 2: ChatPromptTemplate with system + human messages ----
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role}. Answer in at most two short sentences."),
    ("human", "{question}"),
])
chat_chain = chat_prompt | chat_model | StrOutputParser()        # Step 3

# ---- Step 4: normal PromptTemplate on the same model (one flat string, no roles) ----
normal_prompt = PromptTemplate.from_template(
    "You are a helpful {role}. Answer in at most two short sentences.\nQuestion: {question}\nAnswer:"
)
normal_chain = normal_prompt | base_llm | StrOutputParser()

tests = [
    {"role": "science teacher", "question": "Why is the sky blue?"},
    {"role": "travel guide", "question": "Give me one tip for visiting Paris."},
    {"role": "pirate", "question": "How do I make a cup of tea?"},
]

for t in tests:
    print("=" * 70)
    print(f"Role: {t['role']} | Question: {t['question']}")
    print("\n[Messages sent by ChatPromptTemplate]")
    for m in chat_prompt.format_messages(**t):
        print(f"  {m.type:>6}: {m.content}")
    print("\n[ChatPromptTemplate + ChatHuggingFace]\n ", chat_chain.invoke(t).strip())
    print("\n[Normal PromptTemplate + HuggingFacePipeline]\n ", normal_chain.invoke(t).strip())

print("""
Comparison:
- ChatPromptTemplate keeps system and human messages separate; ChatHuggingFace applies the
  model's chat template (special tokens like <|im_start|>), which instruction-tuned models were
  trained on, so they follow the role and the style rules more reliably.
- A normal PromptTemplate produces one flat string. It works, but the model may ignore the
  persona, continue the text oddly or repeat the prompt, especially with small models.
- Chat templates also make multi-turn conversations (system + human + ai + human) easy.
""")
