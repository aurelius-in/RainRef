from fastapi import APIRouter
import time

_start = time.time()

router = APIRouter()

@router.get("/basic")
def basic():
    return {
        "ok": True,
        "uptime_seconds": int(time.time() - _start),
        "requests_total": 0,
    }


