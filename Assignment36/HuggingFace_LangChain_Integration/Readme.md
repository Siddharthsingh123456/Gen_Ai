# Assignment 36: HuggingFace Integration with LangChain

Use open-source HuggingFace models instead of closed APIs (e.g. OpenAI) inside LangChain.

## Project structure
| File | Covers |
|------|--------|
| `hf_utils.py` | Builds HuggingFace-backed LangChain LLMs (local pipeline or HF API) |
| `task1_hf_basics.py` | Getting started: load `google/flan-t5-base`, generate, observe output quality |
| `task2_langchain_hf.py` | HuggingFace with LangChain: `HuggingFacePipeline` wrapper, replace OpenAI in a chain, multiple prompts |
| `task3_chat_prompt.py` | `ChatPromptTemplate` (system + human) with `ChatHuggingFace`, compared with a normal prompt template |
| `test_logic.py` | Offline check of the chains/templates with a fake LLM (no download) |
| `.env.example` | Copy to `.env`: HF token, mode (local/api), model names |

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env     # add HUGGINGFACEHUB_API_TOKEN (token from huggingface.co/settings/tokens)

python task1_hf_basics.py
python task2_langchain_hf.py
python task3_chat_prompt.py
```
The first run downloads the models from HuggingFace (flan-t5-base is about 1 GB, Qwen2.5-0.5B about 1 GB).
After that they run offline on CPU. A GPU makes it faster but is not required.

### Local vs API mode (`HF_MODE` in `.env`)
- `local` (default): the model is downloaded and runs on your machine through `transformers`.
- `api`: calls the model hosted by HuggingFace via `HuggingFaceEndpoint` (needs the token).
  Use this for big models like `mistralai/Mistral-7B-Instruct-v0.2` if your computer is not strong enough:
  set `HF_MODE=api` and `HF_CHAT_MODEL=mistralai/Mistral-7B-Instruct-v0.2`.
  Gated models also require accepting the license on the model page.

## Task 1 – Getting started with HuggingFace models
1. **Load a model:** `google/flan-t5-base` via `AutoTokenizer` + `AutoModelForSeq2SeqLM`.
2. **Generate:** tokenizer -> `model.generate()` -> decode (translation prompt), then the `pipeline` API.
3. **Output quality (typical for flan-t5-base):**
   - Good: translation, factual Q&A, sentiment, short summaries (instruction-style tasks).
   - Weak: long answers, multi-step reasoning, creative writing (short or repetitive output).
   - Pros: free, private, fast on CPU, no API key. Cons: smaller and less capable than large closed models.

## Task 2 – HuggingFace with LangChain
- `HuggingFacePipeline.from_model_id(...)` wraps a transformers pipeline as a LangChain LLM.
- **Replacing OpenAI:** only the model line changes (`ChatOpenAI(...)` -> `get_text_llm()`); the
  chain `PromptTemplate | llm | StrOutputParser()` stays the same. That is the benefit of LangChain's common interface.
- Tested with multiple prompts: question answering (5 questions), translation (3 languages),
  summarization, and `chain.batch()`.

## Task 3 – ChatPromptTemplate with HuggingFace
1. `ChatPromptTemplate.from_messages([("system", ...), ("human", ...)])` with variables `{role}` and `{question}`.
2. `ChatHuggingFace(llm=...)` wraps a HuggingFace LLM so it accepts chat messages and applies the
   model's chat template. Flan-T5 has no chat template, so a chat/instruct model is used here
   (`Qwen/Qwen2.5-0.5B-Instruct` by default, or Mistral-7B-Instruct as in the assignment example).
3. **Comparison with a normal prompt template** (same model, run by `task3_chat_prompt.py`):

| | ChatPromptTemplate + ChatHuggingFace | Normal PromptTemplate + HuggingFacePipeline |
|---|---|---|
| Input | List of role-tagged messages | One flat string |
| Model formatting | Model's own chat template (special tokens) applied automatically | Nothing added; you write the format yourself |
| Following the persona/rules | More reliable for instruction-tuned models | Small models may ignore the role or continue the text oddly |
| Multi-turn chat | Natural (system / human / ai messages) | Awkward, you build the transcript by hand |
| Best for | Chat and instruct models | Simple completions, seq2seq models like Flan-T5 |

## Notes
- `test_logic.py` was run here with a fake LLM and passes (templates, chains and message
  formatting work). The models themselves could not be downloaded in my environment, so the
  model-quality observations above describe typical behaviour of these models. Run the
  scripts on your machine and add your own sample outputs/screenshots if your instructor asks for them.
