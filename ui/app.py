import streamlit as st
from retrieval.retriever import search
from generation.generator import generate_answer
from config import GITHUB_REPOS

st.set_page_config(page_title="RAG Codebase Agent", page_icon="🔍")
st.title("RAG Codebase Agent")
st.caption("Ask questions about your GitHub repositories")

# Sidebar — repo filter
with st.sidebar:
    st.header("Settings")
    repo_options = ["All repos"] + GITHUB_REPOS
    selected = st.selectbox("Scope to repo", repo_options)
    repo_filter = None if selected == "All repos" else selected
    top_k = st.slider("Number of results to retrieve", 3, 10, 5)

# Chat history stored in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
query = st.chat_input("Ask something about your codebase...")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve + generate
    with st.chat_message("assistant"):
        with st.spinner("Searching codebase..."):
            chunks = search(query, repo=repo_filter, top_k=top_k)
            result = generate_answer(query, chunks)

        st.markdown(result["answer"])

        # Show sources in an expander
        with st.expander("Sources"):
            for s in result["sources"]:
                st.markdown(f"- `{s['repo']}` / `{s['source']}` — score: {s['score']}")

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
