from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.db import SessionLocal
from models.entities import KbCard
from services.blob import upload_bytes
from services.kb_embed import embed_text
import uuid
import httpx

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cards")
def search_cards(query: str = Query(""), tags: str = Query(""), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.execute(select(func.count()).select_from(KbCard)).scalar() or 0
    stmt = select(KbCard)
    stmt = stmt.order_by(KbCard.id.asc() if order == "asc" else KbCard.id.desc())
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    q = (query or "").lower()
    tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
    results = []
    for r in rows:
        matches_q = (not q) or q in (r.title or "").lower() or q in (r.body or "").lower()
        matches_tags = (not tag_list) or (set(tag_list).issubset(set((r.tags or []))))
        if matches_q and matches_tags:
            results.append({"id": r.id, "title": r.title, "tags": r.tags or []})
    return {"page": page, "limit": limit, "total": int(total), "results": results}

@router.get("/cards/{card_id}")
def get_card(card_id: str, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    return {"id": obj.id, "title": obj.title, "body": obj.body, "tags": obj.tags or []}

@router.post("/cards")
def upsert_card(card: dict, db: Session = Depends(get_db)):
    cid = card.get("id") or f"kb-{uuid.uuid4().hex[:6]}"
    existing = db.get(KbCard, cid)
    if existing:
        existing.title = card.get("title") or existing.title
        existing.body = card.get("body") or existing.body
        existing.tags = card.get("tags") or existing.tags
        existing.embedding = embed_text(existing.body or "")
        obj = existing
    else:
        obj = KbCard(
            id=cid,
            title=card.get("title", "Untitled"),
            body=card.get("body", ""),
            tags=card.get("tags", []),
            embedding=embed_text(card.get("body", "")),
        )
        db.add(obj)
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": cid, "status": "ok"}

@router.put("/cards/{card_id}")
def update_card(card_id: str, card: dict, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    obj.title = card.get("title") or obj.title
    obj.body = card.get("body") or obj.body
    obj.tags = card.get("tags") or obj.tags
    obj.embedding = embed_text(obj.body or "")
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": card_id, "status": "ok"}

@router.delete("/cards/{card_id}")
def delete_card(card_id: str, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    try:
        db.delete(obj)
        db.commit()
    except Exception:
        db.rollback()
    return {"id": card_id, "deleted": True}

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        blob_name = f"kb-{uuid.uuid4().hex[:8]}-{file.filename}"
        url = upload_bytes("rainref-kb", blob_name, content, file.content_type or "application/octet-stream")
        cid = f"kb-{uuid.uuid4().hex[:6]}"
        obj = KbCard(id=cid, title=file.filename, body=f"Attachment: {url}", tags=["attachment"], embedding=[])
        db.add(obj)
        try:
            db.commit()
        except Exception:
            db.rollback()
        return {"id": cid, "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download")
async def download(url: str = Query(...)):
    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(status_code=400, detail="only http/https URLs supported")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        return Response(content=r.content, media_type=r.headers.get("content-type", "application/octet-stream"))

@router.post("/cards/delete")
def bulk_delete(payload: dict, db: Session = Depends(get_db)):
    ids = payload.get("ids") or []
    deleted = 0
    for cid in ids:
        obj = db.get(KbCard, cid)
        if obj:
            db.delete(obj)
            deleted += 1
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to bulk delete")
    return {"deleted": deleted}
