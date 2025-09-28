from fastapi import APIRouter, Query, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.db import SessionLocal
from models.entities import KbCard
from services.blob import upload_bytes
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cards")
def search_cards(query: str = Query(""), tags: str = Query(""), db: Session = Depends(get_db)):
    stmt = select(KbCard).limit(20)
    rows = db.execute(stmt).scalars().all()
    q = (query or "").lower()
    results = []
    for r in rows:
        if not q or q in (r.title or "").lower() or q in (r.body or "").lower():
            results.append({"id": r.id, "title": r.title, "tags": r.tags or []})
    return {"results": results}

@router.get("/cards/{card_id}")
def get_card(card_id: str, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        return {"error": "not_found"}
    return {"id": obj.id, "title": obj.title, "body": obj.body, "tags": obj.tags or []}

@router.post("/cards")
def upsert_card(card: dict, db: Session = Depends(get_db)):
    cid = card.get("id") or f"kb-{uuid.uuid4().hex[:6]}"
    existing = db.get(KbCard, cid)
    if existing:
        existing.title = card.get("title") or existing.title
        existing.body = card.get("body") or existing.body
        existing.tags = card.get("tags") or existing.tags
        obj = existing
    else:
        obj = KbCard(id=cid, title=card.get("title", "Untitled"), body=card.get("body", ""), tags=card.get("tags", []))
        db.add(obj)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": cid, "status": "ok"}

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    blob_name = f"kb-{uuid.uuid4().hex[:8]}-{file.filename}"
    url = upload_bytes("rainref-kb", blob_name, content, file.content_type or "application/octet-stream")
    cid = f"kb-{uuid.uuid4().hex[:6]}"
    obj = KbCard(id=cid, title=file.filename, body=f"Attachment: {url}", tags=["attachment"])
    db.add(obj)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": cid, "url": url}
