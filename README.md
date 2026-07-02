# Open the app using URL
 https://rag-codebase-agent-4xmzwtfuxz8344hreyglqc.streamlit.app/

# RAG Codebase Agent

Ask questions about your GitHub repository in plain English and get answers with sources.

> "How does login work?" → get an answer with the exact file and line numbers.

---

## How It Works

1. **Ingest** — reads your GitHub repo (code, docs, issues)
2. **Search** — finds the most relevant pieces using embeddings + keyword search
3. **Answer** — sends the results to an LLM and returns an answer with sources

---

## Features

- Ask questions about any GitHub repo
- Searches across code, README, and issues
- Every answer cites the source file and line
- Supports multiple repos

---

## Tech Stack

- **LangChain** — the glue that connects all the pieces together (fetching, searching, prompting the LLM)
- **ChromaDB** — a local database that stores your code as vectors so it can be searched by meaning, not just keywords
- **sentence-transformers** — converts text into vectors locally on your machine, completely free, no API key needed
- **Groq** — free LLM API that generates the final answer (fast, no credit card required)
- **PyGithub** — talks to the GitHub API to download your repo's files, issues, and pull requests
- **Streamlit** — turns the whole thing into a simple chat web page with no frontend work needed

---

## Why Groq and not ChatGPT?

Both Groq and ChatGPT (OpenAI) are AI APIs that can read your code and answer questions. We use Groq because:

| | Groq | OpenAI (ChatGPT) |
|---|---|---|
| **Cost** | Free tier, no credit card | Paid, requires credit card |
| **Speed** | Very fast | Slower |
| **Model** | Llama 3 (Meta, open-source) | GPT-4 (proprietary) |
| **Sign-up** | Just an email | Billing info required |

In short: Groq lets anyone run this project for free, right away. You can swap in OpenAI later if you want better answer quality — just change the API key and update the model name in `config.py`.

---

## Project Structure

```
rag-codebase-agent/
├── ingestion/      # Fetch and chunk GitHub content
├── retrieval/      # Search the vector store
├── generation/     # Build prompt and call LLM
├── ui/             # Streamlit chat interface
└── config.py       # API keys and repo list
```

---

## Setup Guide (from scratch)

### Step 1 — Clone and install dependencies
```bash
git clone <your-repo-url>
cd rag-codebase-agent
pip3 install -r requirements.txt
pip3 install langchain-groq sentence-transformers --user
```

### Step 2 — Create your `.env` file
```bash
cp env.example .env
```
Then open `.env` and fill in:

| Key | Where to get it | Notes |
|---|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys | Free, starts with `gsk_` |
| `GITHUB_TOKEN` | [github.com/settings/tokens](https://github.com/settings/tokens) → Generate new token (classic) | Tick `repo` scope only |
| `GITHUB_REPOS` | Your GitHub repo name(s) | e.g. `myusername/my-project` — leave blank to auto-discover all your repos |

> **Everything is free** — no credit card needed for either Groq or GitHub.

### Step 3 — Index your repo
```bash
python3 ingest.py
```
This fetches your repo's files and issues, converts them to vectors, and stores them locally in `chroma_db/`. Run this once, or re-run whenever your repo changes.

### Step 4 — Run tests (optional but recommended)
```bash
python3 test.py
```
Verifies the full pipeline (ingestion → retrieval → generation) is working.

### Step 5 — Launch the UI
```bash
python3 -m streamlit run ui/app.py
```
Opens a chat interface in your browser. Ask questions about your codebase in plain English.

---

## Example Questions

- *"How does authentication work?"*
- *"How do I run the tests?"*
- *"Are there any open issues about performance?"*
