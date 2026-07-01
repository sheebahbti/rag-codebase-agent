"""
Quick sanity tests for each layer of the pipeline.
Run with: python test.py

Tests (in order):
  1. Config      — are API keys loaded?
  2. ChromaDB    — is the vector store reachable and has data?
  3. Retrieval   — does a simple search return results?
  4. Generation  — does the LLM respond?
  5. End-to-end  — full query → answer flow
"""

import sys


def check(label: str, fn):
    try:
        result = fn()
        print(f"  [PASS] {label}")
        return result
    except Exception as e:
        print(f"  [FAIL] {label}")
        print(f"         {e}")
        sys.exit(1)


# ── 1. Config ──────────────────────────────────────────────────────────────
print("\n[1] Config")

def test_config():
    from config import GROQ_API_KEY, GITHUB_TOKEN, GITHUB_REPOS
    assert GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"), \
        "GROQ_API_KEY missing or invalid in .env"
    assert GITHUB_TOKEN and len(GITHUB_TOKEN) > 10, \
        "GITHUB_TOKEN missing in .env"
    assert len(GITHUB_REPOS) > 0, \
        "GITHUB_REPOS is empty — add at least one repo to .env"
    return GITHUB_REPOS

repos = check("API keys and repos loaded from .env", test_config)


# ── 2. ChromaDB ────────────────────────────────────────────────────────────
print("\n[2] Vector Store")

def test_chroma():
    import chromadb
    from config import CHROMA_DB_PATH, CHROMA_COLLECTION
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(CHROMA_COLLECTION)
    count = collection.count()
    assert count > 0, (
        f"ChromaDB collection '{CHROMA_COLLECTION}' is empty. "
        "Run `python ingest.py` first."
    )
    return count

count = check("ChromaDB reachable and has data", test_chroma)
print(f"         {count} chunks indexed")


# ── 3. Retrieval ───────────────────────────────────────────────────────────
print("\n[3] Retrieval")

def test_retrieval():
    from retrieval.retriever import search
    results = search("how does this project work", top_k=3)
    assert len(results) > 0, "Search returned no results"
    assert "content" in results[0], "Result missing 'content' field"
    assert "source" in results[0], "Result missing 'source' field"
    return results

results = check("Semantic search returns results", test_retrieval)
print(f"         Top result: {results[0]['repo']} / {results[0]['source']} (score: {results[0]['score']})")


# ── 4. Generation ──────────────────────────────────────────────────────────
print("\n[4] Generation")

def test_generation():
    from generation.generator import generate_answer
    fake_chunks = [{
        "content": "def hello(): return 'Hello, world!'",
        "source": "test.py",
        "repo": "test/repo",
        "score": 0.99,
    }]
    result = generate_answer("What does the hello function do?", fake_chunks)
    assert "answer" in result and len(result["answer"]) > 0, "LLM returned empty answer"
    assert "sources" in result, "Result missing sources"
    return result

result = check("LLM generates an answer", test_generation)
print(f"         Answer preview: {result['answer'][:80]}...")


# ── 5. End-to-end ──────────────────────────────────────────────────────────
print("\n[5] End-to-end")

def test_end_to_end():
    from retrieval.retriever import search
    from generation.generator import generate_answer
    query = "What does this project do?"
    chunks = search(query, top_k=3)
    result = generate_answer(query, chunks)
    assert len(result["answer"]) > 0
    return result

result = check("Full query → answer pipeline works", test_end_to_end)
print(f"         Answer preview: {result['answer'][:80]}...")
print(f"         Sources used: {[s['source'] for s in result['sources']]}")


print("\nAll tests passed. The project is working correctly.\n")
