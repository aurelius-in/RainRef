from typing import Dict, Any, Optional
import os
import httpx

class IntercomAdapter:
    name = "intercom"
    def perform(self, payload: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str:
        cfg = config or {}
        base = cfg.get("intercom_base_url") or os.getenv("INTERCOM_BASE_URL")
        token = cfg.get("intercom_token") or os.getenv("INTERCOM_TOKEN")
        if not base or not token:
            return "ic-" + (payload.get("external_id") or "123")
        try:
            data = {
                "message_type": "inapp",
                "body": payload.get("body") or "Hello from RainRef",
                "from": {"type": "user", "id": payload.get("user_id")},
            }
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            url = f"{base.rstrip('/')}/messages"
            with httpx.Client(timeout=10) as client:
                r = client.post(url, json=data, headers=headers)
                r.raise_for_status()
                mid = r.json().get("id")
                return f"ic-{mid}" if mid else "ic-unknown"
        except Exception:
            return "ic-error"
