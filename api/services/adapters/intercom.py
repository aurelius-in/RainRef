from typing import Dict, Any, Optional
import os
import httpx
from .base import http_post_with_retries

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
            r = http_post_with_retries(url, data, headers, timeout=10.0, retries=2)
            try:
                mid = r.json().get("id")
                return f"ic-{mid}" if mid else "ic-unknown"
            except Exception:
                raise RuntimeError(f"Intercom response parse error: status={r.status_code} body={r.text[:200]}")
        except httpx.HTTPError as e:
            raise RuntimeError(f"Intercom HTTP error: {str(e)}")
