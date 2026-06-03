import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, CHROMA_COLLECTION

# Runs locally — no API key needed. Downloads once (~90MB) on first run.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks: list[dict]):
    """
    Convert chunks to vectors and store them in ChromaDB.
    """
    embeddings_model = _model

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(CHROMA_COLLECTION)

    print(f"Embedding {len(chunks)} chunks...")

    # Process in batches of 100 to avoid rate limits
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        texts = [c["content"] for c in batch]
        metadatas = [
            {"source": c["source"], "repo": c["repo"], "type": c["type"]}
            for c in batch
        ]
        ids = [f"{c['repo']}::{c['source']}::{i + j}" for j, c in enumerate(batch)]

        vectors = embeddings_model.encode(texts).tolist()

        collection.add(
            documents=texts,
            embeddings=vectors,
            metadatas=metadatas,
            ids=ids,
        )
        print(f"  Stored batch {i // batch_size + 1} / {-(-len(chunks) // batch_size)}")

    print("Done. All chunks stored in ChromaDB.")
