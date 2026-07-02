import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
st.set_page_config(page_title="RAG Codebase Agent", page_icon="🔍")

from retrieval.retriever import search
from generation.generator import generate_answer
from config import GITHUB_REPOS
st.title("RAG Codebase Agent")
st.caption("Ask questions about your GitHub repositories")

# Sidebar — repo filter
with st.sidebar:
    st.header("Settings")
    repo_options = ["All repos"] + GITHUB_REPOS
    selected = st.selectbox("Scope to repo", repo_options)
    repo_filter = None if selected == "All repos" else selected
    top_k = st.slider("Number of results to retrieve", 3, 10, 5)

    st.divider()
    st.subheader("What's indexed")
    st.markdown("""
**Repos available:**
- `SwimmingPoolCleaningService`
- `MyPortfolio`
- `rag-codebase-agent`
- `AIProjects`
- `MyReminders`

**Content type:** code files & docs only

**Not indexed:** GitHub issues, PRs, comments
    """)

# Chat history stored in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Suggested prompts shown only when chat is empty
SUGGESTED_PROMPTS = [
    "How does the Swimming Pool Cleaning Service work?",
    "What technologies are used in MyPortfolio?",
    "Why was Streamlit chosen for deployment instead of Render?",
    "How does the RAG pipeline work in this project?",
    "What AI projects are in AIProjects repo?",
    "How is the codebase structured?",
]

if not st.session_state.messages:
    st.markdown("#### Suggested questions")
    cols = st.columns(2)
    for i, prompt in enumerate(SUGGESTED_PROMPTS):
        if cols[i % 2].button(prompt, use_container_width=True):
            st.session_state.pending_query = prompt
            st.rerun()

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle prompt button click or typed input
query = st.session_state.pop("pending_query", None) or st.chat_input("Ask something about your codebase...")

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
