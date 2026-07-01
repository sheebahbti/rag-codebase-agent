# What I Learned Building This Project

## What is RAG?

RAG stands for **Retrieval-Augmented Generation**. Instead of asking an AI to answer from memory, you:
1. Search your own data for relevant pieces
2. Give those pieces to the AI as context
3. The AI answers based on *your* data, not its training data

This means the AI can answer questions about *your* private code, even though it has never seen it before.

---

## The 3-Step Pipeline

```
Your GitHub Repo
      ↓
  [Ingestion]   — read files, split into chunks, convert to vectors, store in ChromaDB
      ↓
  [Retrieval]   — convert question to vector, find similar chunks in ChromaDB
      ↓
  [Generation]  — send question + matching chunks to LLM, get an answer with sources
```

---

## Key Concepts

### Embeddings (Vectors)
- Text gets converted into a list of numbers (a "vector") that represents its *meaning*
- Similar meaning = similar numbers = close together in vector space
- This is what makes semantic search work — "how do I log in?" finds "authentication flow" even though the words are different
- We use `sentence-transformers` (free, runs locally) to do this

### Vector Store (ChromaDB)
- A database optimised for storing and searching vectors
- Stores each chunk of code/docs alongside its vector
- At query time: convert question → vector → find nearest chunks
- Runs locally on your machine, no cloud needed

### Chunking
- You can't send an entire codebase to the LLM (too big)
- So you split it into small overlapping pieces (~500 characters each)
- Overlap (50 chars) ensures context isn't lost at chunk boundaries

### LLM (Groq / Llama3)
- The model that reads the retrieved chunks and writes a human-readable answer
- It does NOT search — searching is done separately by ChromaDB
- Groq hosts Llama3 for free with a fast API

### Why Groq instead of OpenAI?
- Groq is free (14,400 requests/day) — no credit card needed
- OpenAI charges per token
- Both use the same LangChain interface — swapping is just a config change

---

## What Makes This More Than Basic RAG

| Feature | Why it matters |
|---|---|
| Reads GitHub issues too | You can ask about bugs, not just code |
| Metadata on every chunk | You can filter by repo, file type, source |
| Multi-repo support | One tool for all your projects |
| Sources in every answer | You can verify the AI didn't make things up |

---

## Tools Used and Why

| Tool | Role | Why chosen |
|---|---|---|
| `sentence-transformers` | Turn text into vectors | Free, runs locally, no API key |
| `ChromaDB` | Store and search vectors | Simple, local, no server needed |
| `LangChain` | Connect all the pieces | Standard RAG framework |
| `langchain-groq` | Call the free LLM | Groq is fastest free LLM API |
| `PyGithub` | Download repo content | Official GitHub API wrapper |
| `Streamlit` | Build the chat UI | No frontend code needed |

---

## Re-ingestion: Keeping the Index Up to Date

`ingest.py` takes a **snapshot** of your repo at the time you run it. ChromaDB stores that snapshot locally in `chroma_db/`.

**When to re-run `python3 ingest.py`:**
- You pushed new code to your repo
- You closed/opened issues you want to query
- You added a new repo to `GITHUB_REPOS`

**What happens when you re-run it:**
- It fetches the latest files and issues from GitHub
- It overwrites the old vectors in ChromaDB with fresh ones
- The UI will immediately reflect the updated code on next query

**Tip:** If you only changed one repo, you can set `GITHUB_REPOS=owner/that-repo` temporarily to re-ingest just that one instead of all repos.

---

## How the `.env` File Works

The `.env` file stores secrets that the app needs but should never be committed to Git.

| Key | What it does |
|---|---|
| `GROQ_API_KEY` | Authenticates your requests to Groq's AI API (free) |
| `GITHUB_TOKEN` | Lets PyGithub read your repos (free, needs `repo` scope) |
| `GITHUB_REPOS` | Comma-separated list of repos to index — leave blank to auto-discover all |

`config.py` reads these at startup using `python-dotenv`. If a key is missing, the relevant feature silently fails or prints an error.

**Security rules:**
- Never commit `.env` to Git (add it to `.gitignore`)
- Never share your keys publicly — regenerate them if you do
- The `env.example` file is safe to commit — it only has placeholder values

---

## Project Setup Steps (Reproduce from Scratch)

1. **Clone the repo and install dependencies**
   ```bash
   pip3 install -r requirements.txt
   pip3 install langchain-groq sentence-transformers --user
   ```

2. **Create `.env` from the example**
   ```bash
   cp env.example .env
   ```

3. **Fill in `.env`**
   - `GROQ_API_KEY` — get free key at [console.groq.com](https://console.groq.com)
   - `GITHUB_TOKEN` — generate at [github.com/settings/tokens](https://github.com/settings/tokens) (tick `repo` scope)
   - `GITHUB_REPOS` — leave blank to index all your repos, or set e.g. `myusername/my-project`

4. **Index your repos**
   ```bash
   python3 ingest.py
   ```

5. **Run tests**
   ```bash
   python3 test.py
   ```

6. **Launch the UI**
   ```bash
   python3 -m streamlit run ui/app.py
   ```

Re-run step 4 any time your repo changes.
