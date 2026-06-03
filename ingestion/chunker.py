from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Split large documents into smaller overlapping chunks.
    Preserves original metadata on every chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # ~500 characters per chunk
        chunk_overlap=50,     # 50 char overlap so context isn't lost at boundaries
    )

    chunks = []
    for doc in documents:
        pieces = splitter.split_text(doc["content"])
        for piece in pieces:
            chunks.append({
                "content": piece,
                "source": doc["source"],
                "repo": doc["repo"],
                "type": doc["type"],
            })

    return chunks
