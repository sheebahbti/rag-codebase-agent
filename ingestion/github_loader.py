from github import Github
from config import GITHUB_TOKEN, SUPPORTED_EXTENSIONS, IGNORED_PATHS


def load_repo(repo_name: str) -> list[dict]:
    """
    Fetch all files and issues from a GitHub repo.
    Returns a list of documents, each with 'content', 'source', and 'repo'.
    """
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(repo_name)
    documents = []

    print(f"[{repo_name}] Fetching files...")
    documents.extend(_fetch_files(repo, repo_name))

    print(f"[{repo_name}] Fetching issues...")
    documents.extend(_fetch_issues(repo, repo_name))

    print(f"[{repo_name}] Total documents: {len(documents)}")
    return documents


def _fetch_files(repo, repo_name: str) -> list[dict]:
    docs = []
    contents = repo.get_contents("")

    while contents:
        item = contents.pop(0)

        # Skip ignored folders
        if any(ignored in item.path for ignored in IGNORED_PATHS):
            continue

        if item.type == "dir":
            contents.extend(repo.get_contents(item.path))
        else:
            ext = "." + item.name.split(".")[-1] if "." in item.name else ""
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            try:
                text = item.decoded_content.decode("utf-8", errors="ignore")
                docs.append({
                    "content": text,
                    "source": item.path,
                    "repo": repo_name,
                    "type": "file",
                })
            except Exception:
                pass  # skip binary or unreadable files

    return docs


def _fetch_issues(repo, repo_name: str) -> list[dict]:
    docs = []
    for issue in repo.get_issues(state="all"):
        body = issue.body or ""
        text = f"Issue #{issue.number}: {issue.title}\n\n{body}"
        docs.append({
            "content": text,
            "source": f"Issue #{issue.number}",
            "repo": repo_name,
            "type": "issue",
            "url": issue.html_url,
        })
    return docs
