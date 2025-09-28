from fastapi import APIRouter, HTTPException, Depends
from services.policy import check_allow
from services.beacon import emit_receipt
from models.db import SessionLocal
from sqlalchemy.orm import Session
from models.entities import AuditLog, Action
import time

router = APIRouter()

_last_exec: dict[str, float] = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/execute")
async def execute(action: dict, db: Session = Depends(get_db)):
    # simple rate limit per action type: 1 per second
    act_type = str(action.get("type", "any"))
    now = time.time()
    last = _last_exec.get(act_type, 0)
    if now - last < 1.0:
        raise HTTPException(status_code=429, detail="too many requests")
    _last_exec[act_type] = now

    allowed = await check_allow(action)
    if not allowed:
        raise HTTPException(status_code=403, detail="action not allowed by policy")

    receipt = emit_receipt(action)
    # write audit log and action record
    db.add(AuditLog(id=receipt, receipt_id=receipt, verified=False))
    db.add(Action(id=f"a-{receipt}", ticket_id=(action.get("ticket_id") or None), type=act_type, params=action.get("params") or {}))
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"ok": True, "beacon_receipt_id": receipt}
