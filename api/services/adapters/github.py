from typing import Dict, Any, Optional
import os
import httpx
from .base import http_post_with_retries

class GithubAdapter:
    name = "github"
    def perform(self, payload: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str:
        cfg = config or {}
        repo = cfg.get("github_repo") or os.getenv("GITHUB_REPO")
        token = cfg.get("github_token") or os.getenv("GITHUB_TOKEN")
        if not repo or not token:
            return "gh-" + (payload.get("external_id") or "123")
        try:
            data = {
                "title": payload.get("title") or "RainRef issue",
                "body": payload.get("body") or "Created by RainRef",
            }
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
            url = f"https://api.github.com/repos/{repo}/issues"
            r = http_post_with_retries(url, data, headers, timeout=10.0, retries=2)
            try:
                num = r.json().get("number")
                return f"gh-{num}" if num else "gh-unknown"
            except Exception:
                raise RuntimeError(f"GitHub response parse error: status={r.status_code} body={r.text[:200]}")
        except httpx.HTTPError as e:
            raise RuntimeError(f"GitHub HTTP error: {str(e)}")
