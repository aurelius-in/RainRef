from fastapi import APIRouter, HTTPException, Depends, Query
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.entities import AuditLog

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{receipt_id}")
def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    row = db.get(AuditLog, receipt_id)
    if not row:
        raise HTTPException(status_code=404, detail="not_found")
    return {"receipt_id": row.receipt_id, "verified": row.verified}

@router.get("/")
def list_audit(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.execute(select(func.count()).select_from(AuditLog)).scalar() or 0
    stmt = select(AuditLog).order_by(AuditLog.id.asc() if order == "asc" else AuditLog.id.desc())
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    return {"page": page, "limit": limit, "total": int(total), "items": [{"id": r.id, "receipt_id": r.receipt_id, "verified": r.verified} for r in rows]}
