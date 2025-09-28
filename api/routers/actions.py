from fastapi import APIRouter, HTTPException, Depends, Query
from services.policy import check_allow
from services.beacon import emit_receipt
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.entities import AuditLog, Action
from models.schemas import ActionRequest
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
async def execute(action: ActionRequest, db: Session = Depends(get_db)):
    act = action.model_dump()
    act_type = act.get("type", "any")
    now = time.time()
    last = _last_exec.get(act_type, 0)
    if now - last < 1.0:
        raise HTTPException(status_code=429, detail="too many requests")
    _last_exec[act_type] = now

    allowed = await check_allow(act)
    if not allowed:
        raise HTTPException(status_code=403, detail="action not allowed by policy")

    receipt = emit_receipt(act)
    db.add(AuditLog(id=receipt, receipt_id=receipt, verified=False))
    db.add(Action(id=f"a-{receipt}", ticket_id=(act.get("ticket_id") or None), type=act_type, params=act.get("params") or {}))
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"ok": True, "beacon_receipt_id": receipt}

@router.get("/history")
def history(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.execute(select(func.count()).select_from(Action)).scalar() or 0
    stmt = select(Action).order_by(Action.id.asc() if order == "asc" else Action.id.desc())
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    return {"page": page, "limit": limit, "total": int(total), "items": [{"id": r.id, "type": r.type, "ticket_id": r.ticket_id} for r in rows]}
