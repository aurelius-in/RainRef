from fastapi import APIRouter, HTTPException, Depends
from models.db import SessionLocal
from sqlalchemy.orm import Session
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
        raise HTTPException(status_code=404, detail="not found")
    return {"receipt_id": row.receipt_id, "verified": row.verified}
