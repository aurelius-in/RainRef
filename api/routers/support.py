from fastapi import APIRouter
from models.schemas import AnswerProposal

router = APIRouter()

@router.post("/answer", response_model=AnswerProposal)
def answer():
    # TODO: triage, retrieval, compose, citations enforced
    return {
        "ticket_id": "t1",
        "answer_md": "Here is the answer with sources.",
        "citations": ["kb:card-123"],
        "actions_suggested": [{"type": "resend_activation", "params": {"user_id": "u-1"}}],
    }
