---
title: GenAI Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
pinned: false
short_description: Streamlit + LangChain chat assistant (Groq / OpenAI)
---

# Assignment 39: GenAI App Deployment

A small GenAI chat assistant (Streamlit + LangChain + Groq/OpenAI) prepared for deployment on
**Streamlit Community Cloud** and **Hugging Face Spaces**.

> The block of text between the `---` lines at the top is the Hugging Face Space configuration
> (Task 2: "Configure README.md"). Streamlit Cloud and GitHub simply ignore it.

## Live URLs (fill in after you deploy)
| Platform | URL |
|----------|-----|
| GitHub repository | `https://github.com/<your-username>/<repo-name>` |
| Streamlit Cloud | `https://<your-app-name>.streamlit.app` |
| Hugging Face Space | `https://huggingface.co/spaces/<your-username>/<space-name>` |

## The app
- Chat with streaming answers, conversation memory (`st.session_state`) and a clear-chat button.
- Sidebar: provider (Groq or OpenAI), model name, assistant mode (general / tutor / code helper / summarizer), temperature.
- **API keys are never in the code.** They are read from the platform's *Secrets* (or pasted in the
  sidebar for a session). Without a key the app starts normally and tells the user what to add.

## Project structure
| File | Purpose |
|------|---------|
| `app.py` | The Streamlit application (Task 1: `app.py`) |
| `llm_factory.py` | Reads secrets (Streamlit secrets or environment variables) and builds the LLM |
| `requirements.txt` | Dependencies installed by both platforms (Task 1: `requirements.txt`) |
| `Dockerfile` | Needed only for Hugging Face Spaces (Streamlit runs through the Docker SDK) |
| `.streamlit/secrets.toml.example` | Template for secrets (the real `secrets.toml` is git-ignored) |
| `.github/workflows/sync_to_hf.yml` | Optional: auto-sync GitHub to the Hugging Face Space |
| `.gitignore`, `.dockerignore` | Keep keys and junk out of Git and Docker |
| `test_offline.py` | Local test without any API key |
| `DEPLOYMENT_GUIDE.md` | Step-by-step deployment for both platforms + troubleshooting |

## Run locally
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml     # add your GROQ_API_KEY
streamlit run app.py
```

## Deployment summary (details in `DEPLOYMENT_GUIDE.md`)
**Task 1 - Streamlit Cloud:** push to GitHub (with `app.py` + `requirements.txt`) -> share.streamlit.io ->
*Create app* -> pick repo, branch `main`, main file `app.py` -> *Advanced settings -> Secrets* -> *Deploy* -> test the URL.

**Task 2 - Hugging Face Spaces:** create a Space (Docker SDK, Streamlit template) -> upload these files or
push/sync from GitHub -> keep the YAML block above in `README.md` -> add the key under *Settings ->
Variables and secrets* -> wait for the build -> test the app.

## Task 3 - Streamlit Cloud vs Hugging Face Spaces

| | Streamlit Community Cloud | Hugging Face Spaces |
|---|---|---|
| Best for | Streamlit apps and dashboards, fastest path from GitHub to a live URL | ML demos and apps that live next to models and datasets on the Hub |
| Frameworks | Streamlit only | Gradio, Docker (which runs Streamlit, FastAPI, anything) and static HTML |
| Deploy method | Connect a GitHub repo; every push redeploys automatically | Git repo hosted by Hugging Face (web upload or `git push`); GitHub sync via an Action |
| Config | Just `app.py` + `requirements.txt` | README YAML block (+ `Dockerfile` for Streamlit) |
| Secrets | App settings -> Secrets (TOML, read via `st.secrets`) | Settings -> Variables and secrets (read as environment variables) |
| Free resources | Limited CPU and memory shared with other apps; no GPU | CPU Basic: 2 vCPU, 16 GB RAM; paid CPU/GPU upgrades available |
| Sleep behaviour | Apps with no traffic for 12 hours go to sleep | Free hardware sleeps after a period of inactivity |
| Privacy | Unlimited public apps, one private app | Public / protected / private visibility (protected and private need paid plans) |
| Cost caveat | Free | Free hardware tier exists, but current docs say creating Docker/Gradio Spaces needs a paid plan, so check your account |

**Pros and cons**
- *Streamlit Cloud* - Pros: simplest setup, automatic redeploy on every git push, built-in secrets UI, free, great
  for demos and portfolios. Cons: Streamlit only, GitHub account required, small resource limits and no GPU, apps go to sleep.
- *Hugging Face Spaces* - Pros: more RAM on the free CPU tier, GPU upgrades when needed, supports many frameworks,
  good visibility in the ML community, easy use of Hub models and datasets. Cons: Streamlit needs a Dockerfile now
  (the built-in Streamlit SDK is deprecated), more configuration, GitHub sync needs extra setup, possible plan
  requirement for Docker Spaces.

**When to use which**
- Choose **Streamlit Cloud** for a quick Streamlit app, a class project, or a dashboard with light compute, especially when the code is on GitHub.
- Choose **Hugging Face Spaces** when the app is an ML demo that should be discoverable on the Hub, needs more memory or a GPU, uses Hub models directly, or uses another framework (Gradio, Docker).
- Many teams deploy to both: Streamlit Cloud for the easy public link, Hugging Face for ML community reach.
