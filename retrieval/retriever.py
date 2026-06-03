import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, CHROMA_COLLECTION

_model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query: str, repo: str = None, top_k: int = 5) -> list[dict]:
    """
    Search ChromaDB for chunks most relevant to the query.
    Optionally filter by a specific repo name.
    Returns a list of results with content and source metadata.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(CHROMA_COLLECTION)

    query_vector = _model.encode(query).tolist()

    where_filter = {"repo": repo} if repo else None

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append({
            "content": doc,
            "source": meta.get("source"),
            "repo": meta.get("repo"),
            "type": meta.get("type"),
            "score": round(1 - dist, 3),  # convert distance to similarity score
        })

    return output
