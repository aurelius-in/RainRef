from fastapi import APIRouter, HTTPException
from services.policy import check_allow
from services.beacon import emit_receipt
import asyncio

router = APIRouter()

@router.post("/execute")
async def execute(action: dict):
    allowed = await check_allow(action)
    if not allowed:
        raise HTTPException(status_code=403, detail="action not allowed by policy")
    receipt = emit_receipt(action)
    return {"ok": True, "beacon_receipt_id": receipt}
