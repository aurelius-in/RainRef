from fastapi import Header, HTTPException
from typing import Optional
from config import settings

async def require_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    expected = getattr(settings, "api_key", None) or getattr(settings, "API_KEY", None)
    if not expected:
        return  # no key configured -> open
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="invalid api key")
