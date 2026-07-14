"""
Push the RampID Detector repo to GitHub using dulwich (pure Python git).
No Xcode Command Line Tools required.

Usage:
    GITHUB_PAT="your_token_here" uv run python push_to_github.py
"""

import os
import sys
from urllib.parse import urlparse

from dulwich.repo import Repo
from dulwich import porcelain

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
REMOTE_URL = "https://github.com/Stigz-115/RampID_Detector.git"


def main():
    pat = os.environ.get("GITHUB_PAT", "").strip()
    if not pat:
        print("ERROR: Set GITHUB_PAT environment variable first.")
        print("Example: GITHUB_PAT='your_token' uv run python push_to_github.py")
        sys.exit(1)

    # Build authenticated URL: https://Stigz-115:<token>@github.com/...
    parsed = urlparse(REMOTE_URL)
    auth_url = f"https://Stigz-115:{pat}@{parsed.netloc}{parsed.path}"

    repo = Repo(REPO_DIR)

    # Ensure we're on main
    current_branch = repo.refs.follow(b"HEAD")[0][1]
    print(f"Current branch: {current_branch.decode()}")

    # Get the commit to push
    commit_sha = repo.refs[current_branch]
    print(f"Commit to push: {commit_sha.decode()}")

    print(f"Pushing to {REMOTE_URL} ...")

    try:
        result = porcelain.push(
            repo,
            auth_url,
            "refs/heads/main",
        )
        print(f"Push result: {result}")
        print("SUCCESS: Repo pushed to GitHub!")
    except Exception as e:
        print(f"Push failed: {e}")
        # Try alternate branch name
        try:
            print("Trying with refs/heads/master ...")
            repo.refs[b"refs/heads/master"] = commit_sha
            result = porcelain.push(
                repo,
                auth_url,
                "refs/heads/master",
            )
            print(f"Push result: {result}")
            print("SUCCESS: Repo pushed to GitHub!")
        except Exception as e2:
            print(f"Also failed: {e2}")
            sys.exit(1)


if __name__ == "__main__":
    main()
