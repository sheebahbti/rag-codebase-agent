from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from config import GROQ_API_KEY


def generate_answer(query: str, context_chunks: list[dict]) -> dict:
    """
    Build a prompt from retrieved chunks and ask the LLM to answer.
    Returns the answer text and the sources used.
    """
    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # free, fast — swap to llama-3.3-70b-versatile for better quality
        groq_api_key=GROQ_API_KEY,
        temperature=0,
    )

    # Build context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        context_parts.append(
            f"[{i}] Source: {chunk['repo']} / {chunk['source']}\n{chunk['content']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "You are a helpful assistant that answers questions about a software codebase. "
        "Use only the context provided. If the answer is not in the context, say so. "
        "Always mention which source file your answer comes from."
    )

    user_prompt = f"Context:\n\n{context}\n\nQuestion: {query}"

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])

    sources = [
        {"repo": c["repo"], "source": c["source"], "score": c["score"]}
        for c in context_chunks
    ]

    return {
        "answer": response.content,
        "sources": sources,
    }
