from typing import Dict, Any

class GithubAdapter:
    name = "github"
    def perform(self, payload: Dict[str, Any]) -> str:
        # simulate creating an issue
        return "gh-" + (payload.get("external_id") or "123")
