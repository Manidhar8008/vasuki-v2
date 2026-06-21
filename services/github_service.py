from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed")

    return result.stdout.strip()

def github_status(query: str = "") -> dict:
    branch = run_git("branch", "--show-current")
    latest_commit = run_git("log", "-1", "--pretty=format:%h | %s")
    remote_url = run_git("remote", "get-url", "origin")
    changed_files = run_git("status", "--short")

    return {
        "tool": "github_status",
        "repository_path": str(PROJECT_ROOT),
        "branch": branch,
        "latest_commit": latest_commit,
        "remote": remote_url,
        "working_tree": changed_files.splitlines() if changed_files else [],
        "clean": changed_files == "",
    }
