# GenAI Learning & Engineering Portfolio

A hands-on learning repository covering Python, data science, machine learning, NLP, embeddings, LangChain, retrieval-augmented generation (RAG), AI agents, and LLM deployment.

> **Learn by building:** 39 independent assignments, each organized around a focused concept or practical project.

## Repository highlights

- 39 assignments from Python fundamentals to LLM deployment
- Python scripts and Jupyter notebooks
- Data analysis, visualization, classical ML, NLP, embeddings, retrieval, chatbots, and agents
- Practical exposure to Streamlit, FastAPI, LangChain, Groq, OpenAI-compatible APIs, Ollama, Hugging Face, vector databases, and Docker

## Assignment roadmap

| # | Assignment | Main concepts |
|---:|---|---|
| 01 | [Python Fundamentals & Collections](Assignment1/) | Lists, tuples, sets, dictionaries |
| 02 | [Python Control Flow](Assignment2/) | Conditions and loops |
| 03 | [Python Functions](Assignment3/) | Reusable functions and program structure |
| 04 | [Python File Handling](Assignment4/) | Reading and writing files |
| 05 | [Python Modules & Packages](Assignment5/) | Imports and modular code |
| 06 | [Python Exception Handling](Assignment6/) | Errors and defensive programming |
| 07 | [Python OOP](Assignment7/) | Classes and object-oriented programming |
| 08 | [Streamlit Applications](Assignment8/) | Interactive Python apps |
| 09 | [NumPy Fundamentals](Assignment9/) | Arrays, operations, and statistics |
| 10 | [Pandas Data Analysis](Assignment10/) | DataFrames and data manipulation |
| 11 | [Matplotlib Visualization](Assignment11/) | Charts and plotting |
| 12 | [Seaborn Visualization](Assignment12/) | Statistical visualization |
| 13 | [Data Gathering, Preprocessing & EDA](Assignment13/) | Data preparation and exploration |
| 14 | [Feature Engineering Pipelines](Assignment14/) | Feature preparation and transformations |
| 15 | [Machine Learning Algorithms & Metrics](Assignment15/) | Regression, classification, evaluation |
| 16 | [NLP Text Preprocessing](Assignment16/) | Preparing text for NLP |
| 17 | [NLP Text Cleaning](Assignment17/) | Normalization and cleaning |
| 18 | [NLP Text Vectorization](Assignment18/) | Numerical text representations |
| 19 | [Word2Vec Embeddings](Assignment19/) | Word representations and similarity |
| 20 | [Movie Recommendation System](Assignment20/) | Recommendation workflows |
| 21 | [LangChain Loaders & Splitters](Assignment21/) | Document ingestion and splitting |
| 22 | [Document Chunking](Assignment22/) | Chunking strategies |
| 23 | [Retrieval-Augmented Generation](Assignment23/) | Retrieval-grounded generation |
| 24 | [LangChain Chatbot](Assignment24/) | Conversational applications |
| 25 | [LangChain Prompting & Chains](Assignment25/) | Prompt templates and chains |
| 26 | [Groq API, RAG & FastAPI](Assignment26/) | API-backed retrieval chatbot |
| 27 | [Conversation History Chatbot](Assignment27/) | Context-aware conversations |
| 28 | [Advanced RAG System](Assignment28/) | Advanced retrieval patterns |
| 29 | [OpenAI & Ollama QA Chatbot](Assignment29/) | Hosted and local model workflows |
| 30 | [Groq Multi-turn RAG Chatbot](Assignment30/) | Multi-turn retrieval chat |
| 31 | [PDF Chat RAG System](Assignment31/) | Question answering over PDFs |
| 32 | [LangGraph AI Agents](Assignment32/) | Agent workflows and state |
| 33 | [SQL AI Agent](Assignment33/) | Natural-language database interaction |
| 34 | [Text Summarization](Assignment34/) | LLM summarization |
| 35 | [Math AI Agent](Assignment35/) | Tool-assisted mathematical reasoning |
| 36 | [Hugging Face & LangChain](Assignment36/) | Model and framework integration |
| 37 | [AstraDB Vector Search & RAG](Assignment37/) | Vector retrieval |
| 38 | [AI Code Assistant](Assignment38/) | Code-focused AI workflows |
| 39 | [LLM Deployment with Docker](Assignment39/) | Packaging and deployment |

## Quick start

### Clone

```bash
git clone https://github.com/Siddharthsingh123456/Gen_Ai.git
cd Gen_Ai
```

### Create an isolated environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Choose an assignment

Open its folder and read its README before installing packages or running code. Dependencies and entry points differ between assignments. If a project includes `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r path/to/requirements.txt
```

Run the command documented by that assignment. Examples include:

```bash
python path/to/script.py
jupyter notebook
streamlit run app.py
uvicorn app:app --reload
```

These are examples, not universal commands for every project.

## Repository quality checks

Run the lightweight validator from the repository root:

```bash
python scripts/validate_repo.py
```

It checks Python source syntax and Jupyter notebook JSON structure. It does not install dependencies, execute notebooks, test external APIs, or verify deployment behavior.

GitHub Actions runs the same structural validation on pushes and pull requests to `main`.

## API keys and security

Some assignments integrate external AI providers or databases.

- Store local credentials in an untracked `.env` file.
- Use environment variables or deployment secret managers.
- Never commit API keys, passwords, access tokens, or private database URIs.
- Use sanitized `.env.example` files where configuration needs documentation.
- Rotate credentials if they are accidentally exposed.
- Do not upload confidential documents or personal data without permission.

## Documentation and contribution

See:
- [Contribution guidelines](CONTRIBUTING.md)
- [Quality roadmap](docs/QUALITY_ROADMAP.md)
- [Assignment README template](templates/ASSIGNMENT_README_TEMPLATE.md)

Keep assignments self-contained, preserve dataset attribution, document real setup commands, and report only tests that were actually run.

## Scope and limitations

This is a collection of independent educational projects, not a single production application. Each assignment may have different dependencies, API requirements, maturity, and limitations. Review its documentation and source before use.

## Author

**Siddharth Singh**

- GitHub: [@Siddharthsingh123456](https://github.com/Siddharthsingh123456)

---

<p align="center"><strong>Learn. Build. Experiment. Improve.</strong></p>
