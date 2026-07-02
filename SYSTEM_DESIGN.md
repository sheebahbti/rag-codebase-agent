# System Design — RAG Codebase Agent

---

## High-Level Architecture

```mermaid
flowchart TD
    GH[("GitHub Repos\n(code, docs, issues)")]
    ING["INGESTION\ningest.py"]
    CHR[("ChromaDB\nVector Store\n1,868 chunks")]
    UI["STREAMLIT UI\nui/app.py"]
    RET["RETRIEVAL\nretrieval/retriever.py"]
    GEN["GENERATION\ngeneration/generator.py"]
    LLM["GROQ LLM\nLlama 3.1 8B"]
    ANS["Answer + Sources\nshown to user"]

    GH -->|"PyGithub API"| ING
    ING -->|"sentence-transformers\n(embed chunks)"| CHR
    UI -->|"user question"| RET
    CHR -->|"top-K similar chunks"| RET
    RET -->|"question + chunks"| GEN
    GEN -->|"prompt"| LLM
    LLM -->|"answer"| ANS
```

---

## Phase 1 — Ingestion (Run Once)

**What happens:** Your GitHub repo is downloaded, split into small pieces, converted to numbers (vectors), and stored locally.

```mermaid
flowchart LR
    A["GitHub Repo\ne.g. SwimmingPoolService"] 
    B["Fetch Files\nPyGithub API"]
    C["Split into Chunks\n~500 chars each\n50 char overlap"]
    D["Convert to Vectors\nsentence-transformers\nall-MiniLM-L6-v2\n(384 numbers per chunk)"]
    E[("Store in ChromaDB\nchunk + vector + metadata")]

    A --> B --> C --> D --> E
```

**Simple example:**

| Step | Example |
|---|---|
| Raw file | `def book_cleaning(date, pool_size): ...` (2,000 chars) |
| After chunking | 4 chunks of ~500 chars with 50-char overlaps |
| After embedding | Each chunk → `[0.12, -0.45, 0.88, ...]` (384 numbers) |
| Stored in ChromaDB | chunk text + vector + `{repo: "SwimmingPool", source: "booking.py"}` |

---

## Phase 2 — Retrieval (Every Query)

**What happens:** Your question is converted to a vector, then ChromaDB finds the chunks whose vectors are most similar (nearest neighbours).

```mermaid
flowchart LR
    Q["User Question\n'How does booking work?'"]
    QV["Question Vector\n[0.09, -0.41, 0.91, ...]\n(384 numbers)"]
    DB[("ChromaDB\n1,868 chunk vectors")]
    RES["Top 5 Chunks\ne.g. booking.py, README.md"]

    Q -->|"sentence-transformers\nsame model as ingestion"| QV
    QV -->|"cosine similarity search"| DB
    DB --> RES
```

**Why this works (simple analogy):**
> Similar *meaning* → similar *numbers* → close together in vector space.
> "How do I book?" finds `booking.py` even if the word "book" doesn't appear — because the *meaning* is close.

---

## Phase 3 — Generation (Every Query)

**What happens:** The retrieved chunks + your question are sent to an LLM as a prompt. The LLM reads them and writes a human answer.

```mermaid
flowchart TD
    Q["User Question"]
    C["Top 5 Chunks\nfrom ChromaDB"]
    P["Prompt\n= system instructions\n+ chunk context\n+ question"]
    LLM["Groq API\nLlama 3.1 8B Instant"]
    A["Answer\n(with source citations)"]

    Q --> P
    C --> P
    P --> LLM --> A
```

**Prompt structure:**

```
You are a helpful assistant that answers questions about a codebase.
Use only the context provided. Always cite the source file.

[1] Source: SwimmingPoolService / booking.py
def book_cleaning(date, pool_size):
    ...

[2] Source: SwimmingPoolService / README.md
To book a cleaning, call the /book endpoint...

Question: How does booking work?
```

---

## Technology Choices

| Component | Technology | Why |
|---|---|---|
| **Vector store** | ChromaDB | Runs locally, no server, no API key, free |
| **Embedding model** | `sentence-transformers/all-MiniLM-L6-v2` | Free, runs on CPU, fast, no API key |
| **LLM** | Groq → Llama 3.1 8B | Free tier (14,400 req/day), no credit card |
| **GitHub access** | PyGithub | Official API wrapper, handles pagination |
| **Orchestration** | LangChain | Standard RAG framework, swappable components |
| **UI** | Streamlit | Zero frontend code, Python only |
| **Deployment** | Streamlit Community Cloud | Free, zero-config for Streamlit apps |

---

## Data Flow Summary

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant R as Retriever
    participant DB as ChromaDB
    participant G as Generator
    participant LLM as Groq LLM

    User->>UI: "How does booking work?"
    UI->>R: query + repo filter
    R->>R: embed query → vector
    R->>DB: find top-5 similar vectors
    DB-->>R: 5 chunks + metadata
    R-->>UI: chunks
    UI->>G: question + chunks
    G->>LLM: formatted prompt
    LLM-->>G: answer text
    G-->>UI: answer + sources
    UI-->>User: displays answer + source files
```

---

## What's Indexed vs Not Indexed

```
✅ Indexed (can answer questions about)        ❌ Not indexed
─────────────────────────────────────         ──────────────────────
• .py, .js, .ts, .md, .html, .css files       • GitHub Issues
• README and documentation                     • Pull Requests
• Config files                                 • Code comments in PRs
• All 5 repos (1,868 chunks total)             • Live/runtime data
```
