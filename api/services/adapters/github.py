from typing import Dict, Any
import os
import httpx

class GithubAdapter:
    name = "github"
    def perform(self, payload: Dict[str, Any]) -> str:
        repo = os.getenv("GITHUB_REPO")
        token = os.getenv("GITHUB_TOKEN")
        if not repo or not token:
            return "gh-" + (payload.get("external_id") or "123")
        try:
            data = {
                "title": payload.get("title") or "RainRef issue",
                "body": payload.get("body") or "Created by RainRef",
            }
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
            url = f"https://api.github.com/repos/{repo}/issues"
            with httpx.Client(timeout=5) as client:
                r = client.post(url, json=data, headers=headers)
                r.raise_for_status()
                num = r.json().get("number")
                return f"gh-{num}" if num else "gh-unknown"
        except Exception:
            return "gh-error"
