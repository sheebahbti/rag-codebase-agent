# How to Test

Follow these steps in order. Each step must pass before moving to the next.

---

## Step 1 — Install packages

```bash
pip install -r requirements.txt
```

**Expected:** no errors. If you see a version conflict, try inside a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2 — Set up your API keys

```bash
cp env.example .env
```

Open `.env` and fill in the three values:

```
OPENAI_API_KEY=sk-...         # from platform.openai.com/api-keys
GITHUB_TOKEN=ghp_...          # from github.com/settings/tokens (read:repo scope)
GITHUB_REPOS=owner/repo-name  # e.g. sheeba/my-project
```

---

## Step 3 — Index your repo

This downloads your repo from GitHub, splits it into chunks, and stores them locally. Run it once (or again if the repo changes).

```bash
python ingest.py
```

**Expected output:**

```
=== Ingesting: owner/repo-name ===
[owner/repo-name] Fetching files...
[owner/repo-name] Fetching issues...
[owner/repo-name] Total documents: 42
  42 documents → 310 chunks

Embedding and storing 310 total chunks...
  Stored batch 1 / 4
  Stored batch 2 / 4
  ...
Done. All chunks stored in ChromaDB.
Ingestion complete! You can now run the UI.
```

---

## Step 4 — Run the automated tests

```bash
python test.py
```

**Expected output:**

```
[1] Config
  [PASS] API keys and repos loaded from .env

[2] Vector Store
  [PASS] ChromaDB reachable and has data
         310 chunks indexed

[3] Retrieval
  [PASS] Semantic search returns results
         Top result: owner/repo / README.md (score: 0.87)

[4] Generation
  [PASS] LLM generates an answer
         Answer preview: The hello function returns the string 'Hello, world!'...

[5] End-to-end
  [PASS] Full query → answer pipeline works
         Answer preview: This project is a ...
         Sources used: ['README.md', 'config.py']

All tests passed. The project is working correctly.
```

---

## Step 5 — Open the chat UI

```bash
streamlit run ui/app.py
```

A browser tab opens at `http://localhost:8501`. Type a question in the chat box and verify:

- An answer appears
- The **Sources** expander shows the file names used

---

## Common errors and fixes

| Error | Cause | Fix |
|---|---|---|
| `OPENAI_API_KEY missing` | `.env` not filled in | Re-check Step 2 |
| `Collection not found` | Ingest never ran | Run Step 3 |
| `ChromaDB collection is empty` | Ingest failed mid-way | Delete `chroma_db/` folder and re-run `ingest.py` |
| `RateLimitError` | OpenAI free tier | Wait a minute and retry, or add billing |
| `401 Unauthorized` (GitHub) | Token missing or wrong scope | Re-generate token with `read:repo` scope |
| `No module named 'langchain'` | Packages not installed | Run Step 1 |
