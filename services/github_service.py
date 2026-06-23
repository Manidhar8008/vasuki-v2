from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")

    return result.stdout.strip()


def get_github_status() -> dict:
    branch = _run_git("branch", "--show-current")
    remote = _run_git("remote", "get-url", "origin")
    latest_commit = _run_git("log", "-1", "--oneline")
    working_tree = _run_git("status", "--porcelain")

    return {
        "tool": "github_status",
        "repository_path": str(PROJECT_ROOT),
        "branch": branch,
        "remote": remote,
        "latest_commit": latest_commit,
        "clean": not bool(working_tree),
        "working_tree": working_tree.splitlines() if working_tree else [],
    }
