import os
import httpx
from typing import Any, Dict

OPA_URL = os.getenv("OPA_URL", "http://opa:8181")

async def check_allow(action: Dict[str, Any]) -> bool | Dict[str, Any]:
    url = f"{OPA_URL}/v1/data/rainref/allow"
    payload = {"input": {"action": action}}
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        # Support richer responses {"allow": bool, "reason": str}
        result = data.get("result")
        if isinstance(result, dict):
            return result
        return {"allow": bool(result), "reason": None}
