from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "data",
    "backups",
    "logs",
    "exports",
}

def search_local_files(query: str, limit: int = 10) -> dict:
    terms = [term.lower() for term in query.split() if len(term) >= 3]
    matches = []

    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if any(part in SKIP_DIRS for part in path.parts):
            continue

        relative_path = str(path.relative_to(PROJECT_ROOT))
        searchable = relative_path.lower()

        if any(term in searchable for term in terms):
            matches.append({
                "path": relative_path,
                "size_bytes": path.stat().st_size,
            })

        if len(matches) >= limit:
            break

    return {
        "tool": "local_search",
        "query": query,
        "count": len(matches),
        "results": matches,
    }
