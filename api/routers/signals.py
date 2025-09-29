from fastapi import APIRouter, Depends, Query, HTTPException, Response\nfrom services.auth import require_api_key
from models.schemas import ProductSignal
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.entities import ProductSignal as Sig
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/emit")
def emit(sig: ProductSignal, db: Session = Depends(get_db)):
    sid = f"s-{uuid.uuid4().hex[:8]}"
    row = Sig(id=sid, origin=sig.origin, type=sig.type, product_area=sig.product_area, strength=sig.strength, evidence_refs=sig.evidence_refs)
    db.add(row)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"ok": True, "id": sid}

@router.get("/")
def list_signals(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), type: str = Query(""), q: str = Query(""), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.execute(select(func.count()).select_from(Sig)).scalar() or 0
    stmt = select(Sig)
    if type:
        stmt = stmt.where(Sig.type == type)
    stmt = stmt.order_by(Sig.id.asc() if order == "asc" else Sig.id.desc())
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    ql = (q or "").lower()
    items = []
    for r in rows:
        if not ql or ql in (r.origin or "").lower():
            items.append({"id": r.id, "type": r.type, "origin": r.origin})
    return {"page": page, "limit": limit, "total": int(total), "items": items}

@router.delete("/{signal_id}")
def delete_signal(signal_id: str, db: Session = Depends(get_db)):
    row = db.get(Sig, signal_id)
    if not row:
        raise HTTPException(status_code=404, detail="not_found")
    try:
        db.delete(row)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to delete")
    return Response(status_code=204)

