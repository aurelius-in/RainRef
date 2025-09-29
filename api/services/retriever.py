from sqlalchemy.orm import Session
from sqlalchemy import select
from models.entities import KbCard
from typing import List, Tuple
import math
try:
    from rapidfuzz.fuzz import token_set_ratio
except Exception:
    # fallback noop scorer
    def token_set_ratio(a: str, b: str) -> float:
        a = (a or "").lower(); b = (b or "").lower()
        return float(sum(1 for t in a.split() if t in b))

def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def retrieve(db: Session, query: str, k: int = 5) -> List[Tuple[str, str, float]]:
    rows = db.execute(select(KbCard)).scalars().all()
    scored: List[Tuple[str, str, float]] = []
    # crude query embedding to leverage stored vectors
    from .kb_embed import embed_text
    qv = embed_text(query or "")
    for r in rows:
        text = (r.title or "") + "\n" + (r.body or "")
        bm25ish = float(token_set_ratio((query or ""), text))
        vecsim = cosine(qv, (r.embedding or [])[:len(qv)])
        score = 0.7 * (bm25ish/100.0) + 0.3 * vecsim
        if score > 0:
            scored.append((r.id, r.body or "", score))
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored[:k]
