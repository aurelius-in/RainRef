from fastapi import APIRouter, Depends, HTTPException
from models.schemas import RefEventIn
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.entities import RefEvent
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events")
def ingest_event(evt: RefEventIn, db: Session = Depends(get_db)):
    rid = f"e-{uuid.uuid4().hex[:8]}"
    row = RefEvent(
        id=rid,
        source=evt.source,
        channel=evt.channel,
        product=evt.product,
        user_ref=evt.user_ref,
        text=evt.text,
        context=evt.context or {},
    )
    db.add(row)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"status": "ok", "id": rid, "normalized": True}

@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    stmt = select(RefEvent).limit(50)
    rows = db.execute(stmt).scalars().all()
    return {"items": [{"id": r.id, "source": r.source, "channel": r.channel, "text": r.text} for r in rows]}

@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)):
    row = db.get(RefEvent, event_id)
    if not row:
        raise HTTPException(status_code=404, detail="not found")
    return {"id": row.id, "source": row.source, "channel": row.channel, "text": row.text, "user_ref": row.user_ref}
