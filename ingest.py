"""
Run this once to index your repos into ChromaDB.
Usage: python ingest.py
"""
from config import GITHUB_REPOS
from ingestion.github_loader import load_repo
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_and_store


def main():
    if not GITHUB_REPOS:
        print("No repos found. Set GITHUB_REPOS=owner/repo in .env, or leave it blank to auto-discover all your repos.")
        return

    all_chunks = []
    for repo_name in GITHUB_REPOS:
        print(f"\n=== Ingesting: {repo_name} ===")
        documents = load_repo(repo_name)
        chunks = chunk_documents(documents)
        print(f"  {len(documents)} documents → {len(chunks)} chunks")
        all_chunks.extend(chunks)

    print(f"\nEmbedding and storing {len(all_chunks)} total chunks...")
    embed_and_store(all_chunks)
    print("\nIngestion complete! You can now run the UI.")


if __name__ == "__main__":
    main()
