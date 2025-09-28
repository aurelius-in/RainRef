import os
import httpx
from typing import Any, Dict

OPA_URL = os.getenv("OPA_URL", "http://localhost:8181")

async def check_allow(action: Dict[str, Any]) -> bool:
    url = f"{OPA_URL}/v1/data/rainref/allow"
    payload = {"input": {"action": action}}
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        return bool(data.get("result", False))
