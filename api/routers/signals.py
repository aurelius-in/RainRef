from fastapi import APIRouter, Depends
from models.schemas import ProductSignal
from models.db import SessionLocal
from sqlalchemy.orm import Session
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
