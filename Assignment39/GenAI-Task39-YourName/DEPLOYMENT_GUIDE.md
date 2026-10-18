# Deployment Guide

You need: a GitHub account, a Streamlit Community Cloud account (sign in with GitHub at
https://share.streamlit.io), a Hugging Face account, and one API key (free Groq key:
https://console.groq.com/keys).

## 0. Test locally first
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml     # put your real key inside
streamlit run app.py
python test_offline.py                                         # optional: works without a key
```

## Task 1: Deploy on Streamlit Cloud

### 1. Push the project to GitHub
Create an empty repository on github.com (e.g. `genai-assistant`, public), then in the project folder:
```bash
git init
git add .
git commit -m "GenAI assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/genai-assistant.git
git push -u origin main
```
Check on GitHub that `app.py` and `requirements.txt` are in the **root** of the repo and that
`.streamlit/secrets.toml` (your real key) is **not** there (the `.gitignore` prevents it).

### 2. Required files
- `requirements.txt` lists every package the app imports (streamlit, langchain-core, langchain-groq, langchain-openai).
- `app.py` is the entry point.

### 3. Deploy
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** -> *Deploy a public app from GitHub*.
3. Repository: `<your-username>/genai-assistant` | Branch: `main` | Main file path: `app.py`.
4. Optional: set a custom subdomain (your URL will be `https://<subdomain>.streamlit.app`).
5. Open **Advanced settings** -> **Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_your_real_key"
   ```
   (Pick the Python version, e.g. 3.11, if asked.)
6. Click **Deploy**. The first build takes a few minutes; watch the logs.

### 4. Test the live URL
- Open the URL, type a question, check that the answer streams in and that follow-ups remember the conversation.
- Change the mode and the temperature in the sidebar. Press *Clear chat*.
- Changing a secret later: app menu -> **Settings -> Secrets** (the app restarts).
- Every `git push` redeploys automatically. Apps with no traffic for 12 hours go to sleep; opening the URL wakes them.

## Task 2: Deploy on Hugging Face Spaces

Streamlit's built-in "Streamlit SDK" on Hugging Face is deprecated; the current way is the **Docker SDK
with the Streamlit template**. This project already contains the right `Dockerfile` and the README header
(`sdk: docker`, `app_port: 8501`).

> **Check your plan:** the current Hugging Face docs say Docker and Gradio Spaces run on compute and need a
> paid plan (PRO) to create, while free accounts can create static Spaces. If the *Create new Space* page lets
> you choose **Docker -> Streamlit** on your account, continue. If it asks you to upgrade, tell your instructor
> and use the Streamlit Cloud deployment as proof of deployment (or ask me for a Gradio version).

### 1. Create a new Space (Streamlit type)
1. https://huggingface.co/new-space
2. Name: `genai-assistant` | License: any | SDK: **Docker** -> template **Streamlit** | Hardware: **CPU Basic (free)** | Visibility: Public.
3. Click **Create Space**.

### 2. Connect your GitHub repository OR upload files
**Option A - upload files (easiest):** Space page -> **Files** -> **Add file -> Upload files**; drag in everything
from this project (`app.py`, `llm_factory.py`, `requirements.txt`, `Dockerfile`, `README.md`, `.dockerignore`),
overwriting the template files, then **Commit changes**.

**Option B - push with git:** a Space is a git repo.
```bash
git remote add space https://huggingface.co/spaces/<hf-username>/genai-assistant
git push space main --force        # username = your HF username, password = a HF access token with "write" role
```

**Option C - connect from GitHub (automatic):** use `.github/workflows/sync_to_hf.yml`. Replace
`YOUR_HF_USERNAME` and `YOUR_SPACE_NAME`, then in GitHub -> *Settings -> Secrets and variables -> Actions* add
the secret `HF_TOKEN` (HF token with write access). Every push to `main` is then mirrored to the Space.

### 3. Configure README.md
The top of `README.md` must keep this block (already included):
```yaml
---
title: GenAI Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
pinned: false
---
```
`sdk: docker` selects the Dockerfile build; `app_port: 8501` tells Hugging Face where Streamlit listens.

Add the API key: Space -> **Settings -> Variables and secrets -> New secret** -> name `GROQ_API_KEY`,
value = your key. (Secrets are private; the app reads them as environment variables.)

### 4. Deploy and test
- Every commit triggers an automatic build; open the **Logs** tab to follow it (status *Building* -> *Running*).
- Open the Space URL `https://huggingface.co/spaces/<hf-username>/genai-assistant`, ask a question, and check streaming and memory.
- Free Spaces go to sleep after a period of inactivity and wake up when visited.

## Troubleshooting
| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` on the platform | Add the package to `requirements.txt` and push again |
| App says "No API key yet" | Add `GROQ_API_KEY` in Secrets (Streamlit Cloud: TOML syntax with quotes; HF: secret name exact) and restart |
| Streamlit Cloud says file not found | Main file path must be `app.py`, and it must be in the repo root |
| HF Space stuck on *Building* / error | Open *Logs*; check the `Dockerfile` and that README has `app_port: 8501` |
| `401` / model errors in the chat | Wrong or expired key, wrong model name, or free quota used up |
| Key accidentally committed | Delete/rotate the key at the provider immediately, then clean the repo |
