from sqlalchemy.orm import Session
from sqlalchemy import select
from models.entities import KbCard
from typing import List, Tuple
try:
    from rapidfuzz.fuzz import token_set_ratio
except Exception:
    # fallback noop scorer
    def token_set_ratio(a: str, b: str) -> float:
        a = (a or "").lower(); b = (b or "").lower()
        return float(sum(1 for t in a.split() if t in b))

def retrieve(db: Session, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
    rows = db.execute(select(KbCard)).scalars().all()
    scored: List[Tuple[str, str, float]] = []
    for r in rows:
        text = (r.title or "") + "\n" + (r.body or "")
        score = float(token_set_ratio(query or "", text))
        if score > 0:
            scored.append((r.id, r.body or "", score))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:k]
