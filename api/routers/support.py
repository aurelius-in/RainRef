from fastapi import APIRouter, Depends, HTTPException
from models.schemas import AnswerProposal, RefEventIn
from models.db import SessionLocal
from sqlalchemy.orm import Session
from services.flow import run_flow
from models.entities import Ticket
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
    proposal, _ = run_flow(db, ref_event)
    if not proposal.citations:
        raise HTTPException(status_code=422, detail="answer must include citations")
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
def list_tickets(db: Session = Depends(get_db)):
    rows = db.execute(db.query(Ticket).statement).fetchall()
    items = []
    for r in rows:
        # r is Row with Ticket columns
        d = dict(r._mapping)
        items.append({"id": d.get("id"), "status": d.get("status"), "ref_event_id": d.get("ref_event_id")})
    return {"items": items}
