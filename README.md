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

## Quickstart

```bash
pip install -r requirements.txt
cp env.example .env   # add your OpenAI key and GitHub token

python ingest.py       # index your repo (run once)
streamlit run ui/app.py
```

---

## Example Questions

- *"How does authentication work?"*
- *"How do I run the tests?"*
- *"Are there any open issues about performance?"*
