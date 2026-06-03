# Outstanding Items

Items that still need to be completed before the project is fully working.

---

## Blockers (must do first)

- [ ] **Fill in `.env` file**
  - Get free Groq API key from https://console.groq.com → API Keys
  - Get GitHub token from https://github.com/settings/tokens (tick `repo` scope)
  - Set `GITHUB_REPOS=owner/repo-name` to the repo(s) you want to index

- [ ] **Update `.env` key name** — the current `.env` still says `OPENAI_API_KEY`, needs to be changed to `GROQ_API_KEY=gsk_...`

---

## Setup (run once after filling .env)

- [ ] **Install new packages**
  ```bash
  pip3 install langchain-groq sentence-transformers --user
  ```

- [ ] **Run ingestion** — indexes your repo into ChromaDB
  ```bash
  python3 ingest.py
  ```

- [ ] **Run tests** — verify the full pipeline works
  ```bash
  python3 test.py
  ```

- [ ] **Launch UI**
  ```bash
  python3 -m streamlit run ui/app.py
  ```

---

## Nice-to-have improvements (future work)

- [ ] Add `.gitignore` to exclude `chroma_db/` and `.env` from commits
- [ ] Add a re-run ingestion script for when the repo changes
- [ ] Try `llama3-70b-8192` on Groq for better quality answers
- [ ] Add a Groq model selector to the Streamlit sidebar
- [ ] Evaluate answer quality using RAGAS metrics
- [ ] Support filtering by file type (e.g. only search `.py` files)
- [ ] Add PR content to the ingestion pipeline (currently only issues)
