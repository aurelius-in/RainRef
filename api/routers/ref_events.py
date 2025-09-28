from fastapi import APIRouter, Depends
from models.schemas import RefEventIn
from models.db import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events")
def ingest_event(evt: RefEventIn, db: Session = Depends(get_db)):
    # TODO: persist in ref_events table
    return {"status": "ok", "normalized": True}
