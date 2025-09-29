from typing import Tuple, Optional
from sqlalchemy.orm import Session
from models.schemas import RefEventIn, AnswerProposal
from .grounder import retrieve_with_citations, compose_answer


def run_flow(db: Session, ref_event: RefEventIn) -> Tuple[AnswerProposal, Optional[str]]:
	query = ref_event.text or ""
	cits = retrieve_with_citations(db, query, k=3)
	if not cits:
		return AnswerProposal(ticket_id="", answer_md="", citations=[], actions_suggested=[]), None
	answer = compose_answer(query, cits)
	citation_ids = [f"kb:{cid}" for cid, _ in cits]
	proposal = AnswerProposal(ticket_id="", answer_md=answer, citations=citation_ids, actions_suggested=[])
	return proposal, None

