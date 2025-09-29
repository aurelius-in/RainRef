from typing import Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.schemas import RefEventIn, AnswerProposal
from .grounder import retrieve_with_citations, compose_answer


def run_flow(db: Session, ref_event: RefEventIn) -> Tuple[AnswerProposal, Optional[str]]:
    query = ref_event.text or ""
    cits = retrieve_with_citations(db, query, k=3)
    answer_md = compose_answer(query, cits)
    citations = [f"kb:{cid}" for cid, _ in cits]

    actions_suggested: list[Dict[str, Any]] = []
    if "activation" in query.lower():
        actions_suggested.append({
            "type": "resend_activation",
            "params": {"user_ref": ref_event.user_ref}
        })

    proposal = AnswerProposal(
        ticket_id="",
        answer_md=answer_md,
        citations=citations,
        actions_suggested=actions_suggested,
    )
    return proposal, None

