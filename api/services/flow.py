from typing import Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.schemas import RefEventIn, AnswerProposal
from .grounder import retrieve_with_citations, compose_answer
from .policy import check_allow


def run_flow(db: Session, ref_event: RefEventIn) -> Tuple[AnswerProposal, Optional[str]]:
    intent = "activation" if "activation" in (ref_event.text or "").lower() else "general"
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
    # annotate with policy preview
    enriched: list[Dict[str, Any]] = []
    for a in actions_suggested:
        # sync wrapper for async policy call not needed here; leave as suggestion only
        enriched.append({**a, "policy_preview": {"allow": True}})

    proposal = AnswerProposal(
        ticket_id="",
        answer_md=answer_md,
        citations=citations,
        actions_suggested=enriched,
    )
    return proposal, None

