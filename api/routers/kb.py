from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text as sql_text
from models.db import SessionLocal
from models.entities import KbCard
from services import blob
from services.kb_embed import embed_text
from models.schemas import KbCardIn
from services.auth import require_admin_jwt
import uuid
import httpx
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/cards")
def search_cards(query: str = Query(""), tags: str = Query(""), page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), order: str = Query("desc"), db: Session = Depends(get_db)):
    q = (query or "").strip()
    tag_list = [t.strip() for t in (tags or "").split(",") if t.strip()]
    offset = (page - 1) * limit

    # Prefer Postgres full-text if a query is provided
    if q:
        # WHERE to_tsvector('english', title || ' ' || body) @@ plainto_tsquery(:q)
        # ORDER BY ts_rank(...) and id for tie-breaker
        where_clause = sql_text("to_tsvector('english', title || ' ' || body) @@ plainto_tsquery(:q)")
        base = select(KbCard).where(where_clause).order_by(sql_text("ts_rank(to_tsvector('english', title || ' ' || body), plainto_tsquery(:q)) DESC, id DESC")).params(q=q)
        rows = db.execute(base.offset(offset).limit(limit)).scalars().all()
        # total via count over same where
        total = db.execute(select(func.count()).select_from(select(KbCard).where(where_clause).subquery()).params(q=q)).scalar() or 0
        # Tag filtering on top (cheap filter)
        out = []
        for r in rows:
            if not tag_list or set(tag_list).issubset(set(r.tags or [])):
                out.append({"id": r.id, "title": r.title, "tags": r.tags or []})
        return {"page": page, "limit": limit, "total": int(total), "results": out}

    # No query: filter by tags only with stable ordering
    rows = db.execute(select(KbCard).order_by(KbCard.id.desc() if order != "asc" else KbCard.id.asc()).offset(offset).limit(limit)).scalars().all()
    total = db.execute(select(func.count()).select_from(KbCard)).scalar() or 0
    results = []
    for r in rows:
        if not tag_list or set(tag_list).issubset(set(r.tags or [])):
            results.append({"id": r.id, "title": r.title, "tags": r.tags or []})
    return {"page": page, "limit": limit, "total": int(total), "results": results}

@router.get("/cards/{card_id}")
def get_card(card_id: str, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    return {"id": obj.id, "title": obj.title, "body": obj.body, "tags": obj.tags or []}

@router.get("/cards/export")
def export_cards(db: Session = Depends(get_db), __: dict = Depends(require_admin_jwt)):
    rows = db.execute(select(KbCard)).scalars().all()
    data = [{"id": r.id, "title": r.title, "body": r.body, "tags": r.tags or []} for r in rows]
    return Response(content=json.dumps(data), media_type="application/json")

@router.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    rows = db.execute(select(KbCard.tags)).all()
    tags = set()
    for (arr,) in rows:
        for t in (arr or []):
            tags.add(t)
    return {"tags": sorted(tags)}

@router.get("/stats")
def kb_stats(db: Session = Depends(get_db)):
    rows = db.execute(select(KbCard.tags)).all()
    tag_counts: dict[str, int] = {}
    total = db.execute(select(func.count()).select_from(KbCard)).scalar() or 0
    for (arr,) in rows:
        for t in (arr or []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = sorted(({"tag": k, "count": int(v)} for k, v in tag_counts.items()), key=lambda x: x["count"], reverse=True)[:10]
    return {"total": int(total), "top_tags": top_tags}

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

@router.patch("/cards/{card_id}")
def patch_card(card_id: str, patch: KbCardIn, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    if patch.title is not None:
        obj.title = patch.title
    if patch.body is not None:
        obj.body = patch.body
    if patch.tags is not None:
        obj.tags = patch.tags
    obj.embedding = embed_text(obj.body or "")
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": card_id, "status": "ok"}

@router.put("/cards/{card_id}")
def put_card(card_id: str, payload: dict, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    obj.title = payload.get("title", obj.title)
    obj.body = payload.get("body", obj.body)
    obj.tags = payload.get("tags", obj.tags)
    obj.embedding = embed_text(obj.body or "")
    try:
        db.commit()
    except Exception:
        db.rollback()
    return {"id": card_id, "status": "ok"}

@router.delete("/cards/{card_id}")
def delete_card(card_id: str, db: Session = Depends(get_db), __: dict = Depends(require_admin_jwt)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    try:
        db.delete(obj)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to delete")
    return {"ok": True}

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        blob_name = f"kb-{uuid.uuid4().hex[:8]}-{file.filename}"
        url = blob.upload_bytes("rainref-kb", blob_name, content, file.content_type or "application/octet-stream")
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

@router.post("/cards/{card_id}/copy")
def copy_card(card_id: str, db: Session = Depends(get_db)):
    obj = db.get(KbCard, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="not_found")
    new_id = f"kb-{uuid.uuid4().hex[:6]}"
    dup = KbCard(id=new_id, title=obj.title + " (copy)", body=obj.body, tags=obj.tags or [], embedding=obj.embedding)
    db.add(dup)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to copy")
    return {"id": new_id}

@router.post("/cards/delete")
def bulk_delete(payload: dict, db: Session = Depends(get_db), __: dict = Depends(require_admin_jwt)):
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
