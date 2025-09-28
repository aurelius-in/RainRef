from fastapi import APIRouter, HTTPException, Depends
from services.policy import check_allow
from services.beacon import emit_receipt
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

@router.post("/execute")
async def execute(action: dict, db: Session = Depends(get_db)):
    allowed = await check_allow(action)
    if not allowed:
        raise HTTPException(status_code=403, detail="action not allowed by policy")
    receipt = emit_receipt(action)
    # write audit log
    row = AuditLog(id=receipt, receipt_id=receipt, verified=False)
    db.add(row)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"ok": True, "beacon_receipt_id": receipt}
