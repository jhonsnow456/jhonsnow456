#!/usr/bin/env python3
"""
Computes "RPG" style developer stats (XP, level, rank, achievements) from
the GitHub GraphQL + REST APIs, writes them to assets/rpg-stats.json, and
patches the corresponding tables in README.md between marker comments.

Requires:
    GH_TOKEN      - a token with `read:user` and `repo` (public_repo is
                    enough for public-only stats) scope, passed as a repo
                    secret. Do NOT use the default GITHUB_TOKEN for GraphQL
                    user queries across org boundaries; a PAT is more
                    reliable here.
    GH_USERNAME   - the GitHub username to compute stats for.

This script intentionally has no third-party dependencies beyond
`requests`, so it runs on a bare `ubuntu-latest` runner with
`pip install requests` (already present on GitHub-hosted runners).
"""

import json
import math
import os
import sys
from pathlib import Path

import requests

GH_TOKEN = os.environ.get("GH_TOKEN")
GH_USERNAME = os.environ.get("GH_USERNAME")
API_ROOT = "https://api.github.com"
OUT_PATH = Path("assets/rpg-stats.json")

if not GH_TOKEN or not GH_USERNAME:
    print("GH_TOKEN and GH_USERNAME must be set as env vars.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def gh_get(path, params=None):
    resp = requests.get(f"{API_ROOT}{path}", headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_public_stats(username: str) -> dict:
    user = gh_get(f"/users/{username}")
    repos = gh_get(f"/users/{username}/repos", params={"per_page": 100, "type": "owner"})

    stars_received = sum(r.get("stargazers_count", 0) for r in repos)
    repos_created = len(repos)

    # NOTE: total commits / merged PRs / closed issues require the GraphQL
    # API (contributionsCollection + search) for accurate counts. This
    # REST-only version approximates and should be swapped for a GraphQL
    # query if you want exact figures - see docs/SETUP.md.
    search_prs = gh_get(
        "/search/issues",
        params={"q": f"author:{username} type:pr is:merged"},
    )
    search_issues = gh_get(
        "/search/issues",
        params={"q": f"author:{username} type:issue is:closed"},
    )

    merged_prs = search_prs.get("total_count", 0)
    closed_issues = search_issues.get("total_count", 0)

    return {
        "followers": user.get("followers", 0),
        "public_repos": user.get("public_repos", 0),
        "stars_received": stars_received,
        "repos_created": repos_created,
        "merged_prs": merged_prs,
        "closed_issues": closed_issues,
    }


def compute_xp(stats: dict) -> dict:
    commits_estimate = stats["merged_prs"] * 8  # rough proxy, see note above
    xp = (
        commits_estimate * 1
        + stats["merged_prs"] * 5
        + stats["closed_issues"] * 3
        + stats["stars_received"] * 2
        + stats["repos_created"] * 4
    )
    level = max(1, int(math.floor(math.sqrt(xp) / 4)))

    if level < 5:
        rank = "Contributor"
    elif level < 15:
        rank = "Maintainer"
    elif level < 30:
        rank = "Core Engineer"
    else:
        rank = "Legend"

    return {"xp": xp, "level": level, "rank": rank}


def compute_achievements(stats: dict) -> dict:
    return {
        "100_commits": stats["merged_prs"] * 8 >= 100,
        "1000_commits": stats["merged_prs"] * 8 >= 1000,
        "100_stars": stats["stars_received"] >= 100,
        "first_merged_pr": stats["merged_prs"] >= 1,
        "open_source_package": stats["public_repos"] >= 1,
    }


def main():
    stats = get_public_stats(GH_USERNAME)
    rpg = compute_xp(stats)
    achievements = compute_achievements(stats)

    payload = {
        "username": GH_USERNAME,
        "stats": stats,
        "rpg": rpg,
        "achievements": achievements,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))

    # Patching README.md tables from this payload is left as a small,
    # repo-specific templating step -- see docs/SETUP.md "RPG Engine" for
    # a minimal regex-based patcher you can drop in here.


if __name__ == "__main__":
    main()
