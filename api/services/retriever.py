from sqlalchemy.orm import Session
from sqlalchemy import select
from models.entities import KbCard
from typing import List, Tuple

def _score(query: str, text: str) -> float:
    if not query or not text:
        return 0.0
    q = query.lower().split()
    t = text.lower()
    return sum(1.0 for tok in q if tok in t)

def retrieve(db: Session, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
    rows = db.execute(select(KbCard)).scalars().all()
    scored: List[Tuple[str, str, float]] = []
    for r in rows:
        score = _score(query, (r.title or "") + "\n" + (r.body or ""))
        if score > 0:
            scored.append((r.id, r.body or "", float(score)))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:k]
