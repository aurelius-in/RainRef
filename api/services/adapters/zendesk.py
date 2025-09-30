from typing import Dict, Any, Optional
import os
import httpx

class ZendeskAdapter:
    name = "zendesk"
    def perform(self, payload: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str:
        cfg = config or {}
        base = cfg.get("zendesk_base_url") or os.getenv("ZENDESK_BASE_URL")
        token = cfg.get("zendesk_token") or os.getenv("ZENDESK_TOKEN")
        if not base or not token:
            return "zd-" + (payload.get("external_id") or "123")
        try:
            data = {
                "ticket": {
                    "subject": payload.get("subject") or "RainRef ticket",
                    "comment": {"body": payload.get("body") or "Created by RainRef"},
                    "priority": payload.get("priority") or "normal",
                }
            }
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            url = f"{base.rstrip('/')}/api/v2/tickets.json"
            with httpx.Client(timeout=10) as client:
                r = client.post(url, json=data, headers=headers)
                r.raise_for_status()
                tid = r.json().get("ticket", {}).get("id")
                return f"zd-{tid}" if tid else "zd-unknown"
        except Exception:
            return "zd-error"
