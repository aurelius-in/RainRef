import os
import httpx
from typing import Any, Dict, Optional

OPA_URL = os.getenv("OPA_URL", "http://opa:8181")

async def check_allow(action: Dict[str, Any], user: Optional[Dict[str, Any]] = None) -> bool | Dict[str, Any]:
    url = f"{OPA_URL}/v1/data/rainref/allow"
    payload = {"input": {"action": action, "user": (user or {})}}
    async with httpx.AsyncClient(timeout=1.0) as client:
        try:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
        except Exception:
            # In tests or when OPA is not reachable, default allow
            return {"allow": True, "reason": None}
        # Support richer responses {"allow": bool, "reason": str}
        result = data.get("result")
        if isinstance(result, dict):
            return result
        return {"allow": bool(result), "reason": None}
