import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Parse comma-separated list of repos
GITHUB_REPOS = [
    r.strip()
    for r in os.getenv("GITHUB_REPOS", "").split(",")
    if r.strip()
]

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
