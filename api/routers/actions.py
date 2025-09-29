from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from services import policy
from services.beacon import emit_receipt
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.entities import AuditLog, Action
from models.schemas import ActionRequest
from config import settings
import time
from services.auth import require_admin_jwt

router = APIRouter()

_exec_times: dict[str, list[float]] = {}

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
    win = settings.rate_limit_window_sec
    maxn = settings.rate_limit_per_window
    arr = _exec_times.get(act_type, [])
    arr = [t for t in arr if now - t < win]
    if len(arr) >= maxn:
        resp = JSONResponse(status_code=429, content={"detail": "too many requests"})
        resp.headers["X-RateLimit-Limit"] = str(maxn)
        resp.headers["X-RateLimit-Remaining"] = str(0)
        resp.headers["X-RateLimit-Window-Seconds"] = str(win)
        return resp
    arr.append(now)
    _exec_times[act_type] = arr

    policy_result = await policy.check_allow(act)
    allowed = policy_result.get("allow") if isinstance(policy_result, dict) else bool(policy_result)
    if not allowed:
        reason = policy_result.get("reason") if isinstance(policy_result, dict) else None
        raise HTTPException(status_code=403, detail=reason or "action not allowed by policy")

    receipt = emit_receipt(act)
    db.add(AuditLog(id=receipt, receipt_id=receipt, verified=False))
    db.add(Action(id=f"a-{receipt}", ticket_id=(act.get("ticket_id") or None), type=act_type, params=act.get("params") or {}))
    try:
        db.commit()
    except Exception:
        db.rollback()
    resp = JSONResponse(status_code=200, content={"ok": True, "beacon_receipt_id": receipt})
    resp.headers["X-RateLimit-Limit"] = str(maxn)
    resp.headers["X-RateLimit-Remaining"] = str(max(0, maxn - len(arr)))
    resp.headers["X-RateLimit-Window-Seconds"] = str(win)
    return resp

@router.get("/history")
def history(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.execute(select(func.count()).select_from(Action)).scalar() or 0
    stmt = select(Action).order_by(Action.id.asc() if order == "asc" else Action.id.desc())
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    items = []
    for r in rows:
        receipt_id = r.id[2:] if r.id.startswith("a-") else r.id
        items.append({"id": r.id, "receipt_id": receipt_id, "type": r.type, "ticket_id": r.ticket_id})
    return {"page": page, "limit": limit, "total": int(total), "items": items}

@router.get("/history/by-type")
def history_by_type(type: str, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    base = select(Action).where(Action.type == type)
    total = db.execute(select(func.count()).select_from(base.subquery())).scalar() or 0
    rows = db.execute(base.order_by(Action.id.desc()).offset(offset).limit(limit)).scalars().all()
    items = [{"id": r.id, "type": r.type, "ticket_id": r.ticket_id} for r in rows]
    return {"page": page, "limit": limit, "total": int(total), "items": items}
