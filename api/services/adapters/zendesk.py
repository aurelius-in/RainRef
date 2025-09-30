from typing import Dict, Any, Optional
import os
import httpx
from .base import http_post_with_retries

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
            r = http_post_with_retries(url, data, headers, timeout=10.0, retries=2)
            try:
                tid = r.json().get("ticket", {}).get("id")
                return f"zd-{tid}" if tid else "zd-unknown"
            except Exception:
                raise RuntimeError(f"Zendesk response parse error: status={r.status_code} body={r.text[:200]}")
        except httpx.HTTPError as e:
            raise RuntimeError(f"Zendesk HTTP error: {str(e)}")
