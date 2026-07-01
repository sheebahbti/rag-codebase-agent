import os
from dotenv import load_dotenv

load_dotenv()

# Support both .env (local) and Streamlit secrets (deployed)
def _get_secret(key: str) -> str:
    try:
        import streamlit as st
        return st.secrets.get(key) or os.getenv(key, "")
    except Exception:
        return os.getenv(key, "")

GROQ_API_KEY = _get_secret("GROQ_API_KEY")
GITHUB_TOKEN = _get_secret("GITHUB_TOKEN")


def _resolve_repos() -> list[str]:
    """Return the list of repos to index.
    If GITHUB_REPOS is blank or '*', auto-discover all repos for the
    authenticated GitHub user.
    """
    raw = _get_secret("GITHUB_REPOS").strip()
    if raw and raw != "*":
        return [r.strip() for r in raw.split(",") if r.strip()]

    # Auto-discover all repos the token has access to
    if not GITHUB_TOKEN:
        print("[config] No GITHUB_TOKEN set — skipping repo discovery (using pre-built index)")
        return []
    try:
        from github import Github
        gh = Github(GITHUB_TOKEN)
        user = gh.get_user()
        repos = [repo.full_name for repo in user.get_repos(type="owner")]
        print(f"[config] Auto-discovered {len(repos)} repos for '{user.login}'")
        return repos
    except Exception as e:
        print(f"[config] Failed to auto-discover repos: {e}")
        return []


GITHUB_REPOS = _resolve_repos()

# Where ChromaDB stores data locally
CHROMA_DB_PATH = "./chroma_db"
CHROMA_COLLECTION = "codebase"

# File extensions to index (skip binaries, lockfiles, etc.)
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".go", ".java", ".rb", ".rs", ".cpp",
    ".c", ".h", ".md", ".txt", ".yaml", ".yml"
}

# Files/folders to ignore
IGNORED_PATHS = {
    "node_modules", ".git", "dist", "build",
    "__pycache__", ".venv", "venv", "package-lock.json"
}
