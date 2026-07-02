# Outstanding Items

---

## Completed

- [x] **`.env` key name fixed** — changed from `OPENAI_API_KEY` to `GROQ_API_KEY`
- [x] **Groq API key added** to `.env`
- [x] **GitHub token added** to `.env`
- [x] **Auto-discover repos** — leaving `GITHUB_REPOS` blank now auto-fetches all repos for the token's GitHub user
- [x] **README setup guide** — full step-by-step instructions added

---

## Next Steps (do these in order)

- [x] **Install packages** — Streamlit 1.37.1, langchain-groq confirmed installed

- [x] **Run ingestion** — ChromaDB has 1,238 chunks indexed in `codebase` collection

- [ ] **Run tests** — verify the full pipeline works
  ```bash
  python3 test.py
  ```

- [ ] **Launch UI** ← *you are here*
  ```bash
  streamlit run ui/app.py
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
