from fastapi import APIRouter
from models.schemas import ProductSignal

router = APIRouter()

@router.post("/emit")
def emit(sig: ProductSignal):
    # TODO: persist + forward to RainScout/Jira/Linear
    return {"ok": True}
