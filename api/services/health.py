import os
import httpx
from sqlalchemy import text
from . import __package__  # noqa: F401
from models.db import engine

async def check_all() -> dict:
    db_ok = True
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    opa_url = os.getenv("OPA_URL", "http://localhost:8181")
    opa_ok = True
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            r = await client.get(f"{opa_url}/health")
            opa_ok = r.status_code < 500
    except Exception:
        opa_ok = False
    return {"db": db_ok, "opa": opa_ok}
