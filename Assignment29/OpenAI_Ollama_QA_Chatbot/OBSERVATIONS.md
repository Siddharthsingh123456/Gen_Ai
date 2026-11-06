# Assignment 29 - Observations & Insights

## 1. When to prefer OpenAI models

I would prefer OpenAI when I need a hosted model, strong general-purpose responses, and I do not want to manage the model locally.

## 2. When to prefer open-source models

I would prefer Ollama when local execution, privacy, offline use, or avoiding per-request API charges is important.

## 3. Trade-offs in production

OpenAI normally needs an internet connection and API credentials and can create usage costs. Ollama requires local hardware and model storage, but the data can remain on the local machine.

## 4. Cost and scalability

A hosted API is convenient to scale, while local Ollama avoids API charges but uses local CPU/GPU/RAM resources.

## 5. Why ChatPromptTemplate is useful

ChatPromptTemplate keeps the system instruction, conversation history, and current user question in a clear structure. This is easier to maintain than manually joining strings.

## 6. Actual observations

Complete this section after running the project. Do not invent model responses, latency values, or screenshots.
