from fastapi import APIRouter, Depends, HTTPException, Query, Response
from models.schemas import RefEventIn
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
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
def list_events(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), q: str = Query(""), source: str = Query(""), channel: str = Query(""), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    stmt = select(RefEvent)
    if source:
        stmt = stmt.where(RefEvent.source == source)
    if channel:
        stmt = stmt.where(RefEvent.channel == channel)
    stmt = stmt.order_by(RefEvent.id.asc() if order == "asc" else RefEvent.id.desc())
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    ql = (q or "").lower()
    items = []
    for r in rows:
        if not ql or ql in (r.text or "").lower():
            items.append({"id": r.id, "source": r.source, "channel": r.channel, "text": r.text})
    return {"page": page, "limit": limit, "total": int(total), "items": items}

@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)):
    row = db.get(RefEvent, event_id)
    if not row:
        raise HTTPException(status_code=404, detail="not_found")
    return {"id": row.id, "source": row.source, "channel": row.channel, "text": row.text, "user_ref": row.user_ref}

@router.delete("/events/{event_id}")
def delete_event(event_id: str, db: Session = Depends(get_db)):
    row = db.get(RefEvent, event_id)
    if not row:
        raise HTTPException(status_code=404, detail="not_found")
    try:
        db.delete(row)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to delete")
    return {"id": event_id, "deleted": True}

@router.get("/events/export")
def export_events(db: Session = Depends(get_db)):
    rows = db.execute(select(RefEvent)).scalars().all()
    header = "id,source,channel,user_ref,text\n"
    lines = [header]
    for r in rows:
        text = (r.text or "").replace("\n", " ").replace(",", " ")
        user_ref = (r.user_ref or "").replace(",", " ")
        lines.append(f"{r.id},{r.source},{r.channel},{user_ref},{text}\n")
    csv_data = "".join(lines)
    return Response(content=csv_data, media_type="text/csv")
