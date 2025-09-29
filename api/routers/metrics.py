from fastapi import APIRouter

router = APIRouter()

@router.get("/basic")
def basic():
    return {"ok": True}


