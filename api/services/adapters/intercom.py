from typing import Dict, Any

class IntercomAdapter:
    name = "intercom"
    def perform(self, payload: Dict[str, Any]) -> str:
        # simulate sending a message
        return "ic-" + (payload.get("external_id") or "123")
