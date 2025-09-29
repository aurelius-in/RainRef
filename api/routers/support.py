from fastapi import APIRouter, Depends, HTTPException, Query, Response
from models.schemas import AnswerProposal, RefEventIn
from models.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from services.flow import run_flow
from models.entities import Ticket, Action
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/answer", response_model=AnswerProposal)
def answer(ref_event: RefEventIn = None, db: Session = Depends(get_db)):
    ref_event = ref_event or RefEventIn(source="support", channel="inbox", text="help", user_ref=None)
    tid = f"t-{uuid.uuid4().hex[:8]}"
    t = Ticket(id=tid, ref_event_id=None, status="draft")
    db.add(t)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to create ticket")

    proposal, _ = run_flow(db, ref_event)
    if not proposal.citations:
        raise HTTPException(status_code=422, detail="answer must include citations")
    proposal = AnswerProposal(**{**proposal.model_dump(), "ticket_id": tid})
    return proposal

@router.post("/tickets")
def create_ticket(payload: dict, db: Session = Depends(get_db)):
    tid = f"t-{uuid.uuid4().hex[:8]}"
    t = Ticket(id=tid, ref_event_id=payload.get("ref_event_id"), status=payload.get("status", "open"))
    db.add(t)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to create ticket")
    return {"id": tid, "status": t.status}

@router.get("/tickets")
def list_tickets(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100), status: str = Query(""), q: str = Query(""), order: str = Query("desc"), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    stmt = select(Ticket)
    if status:
        stmt = stmt.where(Ticket.status == status)
    stmt = stmt.order_by(Ticket.id.asc() if order == "asc" else Ticket.id.desc())
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()
    ql = (q or "").lower()
    items = []
    for r in rows:
        if not ql or ql in (r.id or "").lower() or ql in (r.ref_event_id or "").lower():
            items.append({"id": r.id, "status": r.status, "ref_event_id": r.ref_event_id})
    return {"page": page, "limit": limit, "total": int(total), "items": items}

@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    t = db.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="not_found")
    return {"id": t.id, "status": t.status, "ref_event_id": t.ref_event_id}

@router.get("/tickets/{ticket_id}/actions")
def list_ticket_actions(ticket_id: str, db: Session = Depends(get_db)):
    rows = db.execute(select(Action).where(Action.ticket_id == ticket_id).order_by(Action.id.desc())).scalars().all()
    return {"items": [{"id": a.id, "type": a.type, "params": a.params} for a in rows]}

@router.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, payload: dict, db: Session = Depends(get_db)):
    t = db.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="not_found")
    t.status = payload.get("status", t.status)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to update ticket")
    return {"id": t.id, "status": t.status}

@router.post("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: str, db: Session = Depends(get_db)):
    t = db.get(Ticket, ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="not_found")
    t.status = "closed"
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to close ticket")
    return {"id": t.id, "status": t.status}

@router.get("/tickets/export")
def export_tickets(db: Session = Depends(get_db)):
    rows = db.execute(select(Ticket)).scalars().all()
    header = "id,status,ref_event_id\n"
    lines = [header]
    for t in rows:
        lines.append(f"{t.id},{t.status},{t.ref_event_id or ''}\n")
    return Response(content="".join(lines), media_type="text/csv")
