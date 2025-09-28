from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RefEventIn(BaseModel):
    source: str
    channel: str
    product: Optional[str] = None
    user_ref: Optional[str] = None
    text: str
    context: Optional[Dict[str, Any]] = None

class AnswerProposal(BaseModel):
    ticket_id: str
    answer_md: str
    citations: List[str] = Field(default_factory=list)
    actions_suggested: List[Dict[str, Any]] = Field(default_factory=list)

class ProductSignal(BaseModel):
    origin: str
    type: str
    product_area: Optional[str] = None
    strength: float = 0.0
    evidence_refs: List[str] = Field(default_factory=list)
