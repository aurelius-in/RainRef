from typing import Dict, Any

class ZendeskAdapter:
    name = "zendesk"
    def perform(self, payload: Dict[str, Any]) -> str:
        # simulate creating a ticket and return id
        return "zd-" + (payload.get("external_id") or "123")
