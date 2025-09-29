from typing import Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.schemas import RefEventIn, AnswerProposal
from .grounder import retrieve_with_citations, compose_answer
from .policy import check_allow
from .beacon import emit_receipt


def triage(evt: RefEventIn) -> Dict[str, Any]:
    return {"intent": "friction" if "activation" in (evt.text or "").lower() else "general"}


def ground(db: Session, evt: RefEventIn) -> Tuple[str, list[str]]:
    cits = retrieve_with_citations(db, evt.text or "", k=3)
    cites = [f"kb:{cid}" for cid, _ in cits]
    ans = compose_answer(evt.text or "", cits)
    return ans, cites


async def plan(evt: RefEventIn) -> list[Dict[str, Any]]:
    actions: list[Dict[str, Any]] = []
    if "activation" in (evt.text or "").lower():
        actions.append({"type": "resend_activation", "params": {"user_id": evt.user_ref or "unknown"}})
    return actions


async def gate(actions: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    gated: list[Dict[str, Any]] = []
    for a in actions:
        res = await check_allow(a)
        allow = bool(res.get("allow") if isinstance(res, dict) else res)
        a = {**a, "allowed": allow, "policy_reason": (res.get("reason") if isinstance(res, dict) else None)}
        gated.append(a)
    return gated


def maybe_execute(actions: list[Dict[str, Any]]) -> Optional[str]:
    for a in actions:
        if a.get("allowed"):
            return emit_receipt(a)
    return None


async def run_flow(db: Session, ref_event: RefEventIn) -> Tuple[AnswerProposal, Optional[str]]:
    _ = triage(ref_event)
    answer_md, citations = ground(db, ref_event)
    actions = await plan(ref_event)
    gated = await gate(actions)
    receipt = maybe_execute(gated)
    proposal = AnswerProposal(ticket_id="", answer_md=answer_md, citations=citations, actions_suggested=gated)
    return proposal, receipt

