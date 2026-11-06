# GenAI Learning & Engineering Portfolio

A structured, hands-on collection of Python, data science, machine learning, NLP, LangChain, RAG, AI agents, and LLM deployment assignments.

> **Goal:** Learn by building. Each assignment is organized as a small, focused project with source code, notebooks, datasets or sample data, and project-specific instructions where available.

## Repository at a glance

- **39 assignments** covering Python fundamentals through LLM deployment
- Python scripts and Jupyter notebooks
- Data analysis, visualization, classical ML, NLP, embeddings, retrieval, chatbots, and agents
- Examples using tools and platforms such as Streamlit, FastAPI, LangChain, Groq, OpenAI, Ollama, Hugging Face, vector databases, and Docker

## Learning roadmap

| Assignment | Topic | Focus |
|---:|---|---|
| 01 | Python Fundamentals & Collections | Lists, tuples, sets, dictionaries |
| 02 | Python Control Flow | Conditions and loops |
| 03 | Python Functions | Reusable functions and program structure |
| 04 | Python File Handling | Reading and writing files |
| 05 | Python Modules & Packages | Imports and modular code |
| 06 | Python Exception Handling | Errors and defensive programming |
| 07 | Python OOP | Classes and object-oriented programming |
| 08 | Streamlit Applications | Interactive Python apps |
| 09 | NumPy Fundamentals | Arrays, operations and statistics |
| 10 | Pandas Data Analysis | DataFrames and data manipulation |
| 11 | Matplotlib Visualization | Charts and plotting |
| 12 | Seaborn Visualization | Statistical visualization |
| 13 | Data Gathering, Preprocessing & EDA | Data preparation and exploration |
| 14 | Feature Engineering Pipelines | Feature preparation and transformations |
| 15 | Machine Learning Algorithms & Metrics | Regression, classification and evaluation |
| 16 | NLP Text Preprocessing | Preparing text for NLP |
| 17 | NLP Text Cleaning | Normalization and cleaning |
| 18 | NLP Text Vectorization | Turning text into numerical features |
| 19 | Word2Vec Embeddings | Word representations and similarity |
| 20 | Movie Recommendation System | Recommendation workflows |
| 21 | LangChain Loaders & Splitters | Document ingestion and splitting |
| 22 | Document Chunking | Chunking strategies |
| 23 | Retrieval-Augmented Generation | Retrieval-grounded generation |
| 24 | LangChain Chatbot | Conversational applications |
| 25 | LangChain Prompting & Chains | Prompt templates and chains |
| 26 | Groq API, RAG & FastAPI | API-backed retrieval chatbot |
| 27 | Conversation History Chatbot | Context-aware conversations |
| 28 | Advanced RAG System | Advanced retrieval patterns |
| 29 | OpenAI & Ollama QA Chatbot | Hosted and local model workflows |
| 30 | Groq Multi-turn RAG Chatbot | Multi-turn retrieval chat |
| 31 | PDF Chat RAG System | Question answering over PDFs |
| 32 | LangGraph AI Agents | Agent workflows and state |
| 33 | SQL AI Agent | Natural-language database interaction |
| 34 | Text Summarization | LLM summarization |
| 35 | Math AI Agent | Tool-assisted mathematical reasoning |
| 36 | Hugging Face & LangChain | Model and framework integration |
| 37 | AstraDB Vector Search & RAG | Vector retrieval |
| 38 | AI Code Assistant | Code-focused AI workflows |
| 39 | LLM Deployment with Docker | Packaging and deployment |

## Repository structure

Assignments are kept independent so that their dependencies and instructions do not become mixed together.

```text
Gen_Ai/
├── Assignment1/
│   └── Python_Fundamentals_Collections/
├── Assignment2/
│   └── Python_Control_Flow/
├── ...
├── Assignment39/
│   └── LLM_Deployment_Docker/
├── .github/
│   └── workflows/
├── scripts/
│   └── validate_repo.py
├── .editorconfig
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

Some assignments also contain notebooks, datasets, deployment guides, or supporting files at the assignment root. Those are retained where the project needs them.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Siddharthsingh123456/Gen_Ai.git
cd Gen_Ai
```

### 2. Choose an assignment

Open the relevant `AssignmentN` folder and read its README before running the code. Not every assignment uses the same dependencies or entry point.

### 3. Create an isolated environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install only the dependencies required by the selected assignment. If that assignment has a `requirements.txt`, use:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the relevant entry point

Use the exact command documented in that assignment's README. Examples include:

```bash
python path/to/script.py
jupyter notebook
streamlit run app.py
uvicorn app:app --reload
```

The commands above are examples, not universal commands for every assignment.

## API keys and secrets

Some projects use paid or hosted AI services. Configure credentials through environment variables or the platform's secret manager.

- Never commit real API keys, passwords, access tokens, or private credentials.
- Keep local values in an untracked `.env` file.
- Commit a sanitized `.env.example` when a project needs to document required variables.
- Use placeholders in examples and documentation.
- Rotate any credential that has accidentally been published.

Typical variable names include `OPENAI_API_KEY`, `GROQ_API_KEY`, and provider-specific database credentials. Only set the variables required by the selected project.

## Quality checks

Run the repository validator from the root:

```bash
python scripts/validate_repo.py
```

It checks Python source syntax and the JSON structure of Jupyter notebooks. It does not install project dependencies or prove that external APIs, datasets, models, or deployments work.

## Learning and contribution standards

- Keep each assignment self-contained.
- Prefer descriptive filenames and clear folder names.
- Document prerequisites, setup, environment variables, run commands, and expected outputs.
- Do not commit virtual environments, caches, secrets, generated model weights, or unnecessary large artifacts.
- Preserve source attribution and dataset licenses.
- Explain important logic with readable code and meaningful comments.
- Add tests for reusable logic and bug fixes where practical.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution checklist.

## Repository improvement plan

The repository is being upgraded in phases so that original assignment work and working project behavior are preserved. See the [quality roadmap](docs/QUALITY_ROADMAP.md) for the audit checklist and [assignment README template](templates/ASSIGNMENT_README_TEMPLATE.md) for consistent project documentation.

## Current scope and limitations

This repository is a learning portfolio, not one unified production application. Each assignment may have different dependencies, API requirements, maturity, and deployment instructions. Review the individual project before using it.

## Author

**Siddharth Singh**

GitHub: [@Siddharthsingh123456](https://github.com/Siddharthsingh123456)

---

If this repository helps you learn, explore the assignments, try the projects, and share constructive feedback.
