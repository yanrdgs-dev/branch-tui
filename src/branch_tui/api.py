import os

import httpx


async def fetch_issues(owner: str, repo: str):
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return [issue for issue in response.json() if "pull_request" not in issue]
