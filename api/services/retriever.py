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
    candidates: List[Tuple[str, str, float]] = []
    # crude query embedding to leverage stored vectors
    from .kb_embed import embed_text
    qv = embed_text(query or "")
    for r in rows:
        text = (r.title or "") + "\n" + (r.body or "")
        bm25ish = float(token_set_ratio((query or ""), text))
        vecsim = cosine(qv, (r.embedding or [])[:len(qv)])
        # stage 1: lexical
        lex_score = bm25ish / 100.0
        # stage 2: semantic rerank
        hybrid = 0.6 * lex_score + 0.4 * vecsim
        candidates.append((r.id, r.body or "", hybrid))
    # take top 2k for rerank; here k may be small so use 5x buffer
    buffer = max(k * 5, 10)
    candidates.sort(key=lambda x: x[2], reverse=True)
    top = candidates[:buffer]
    # final rerank emphasizes diversity lightly by penalizing near-duplicates
    final: List[Tuple[str, str, float]] = []
    seen_ids: set[str] = set()
    for cid, body, score in top:
        if cid in seen_ids:
            continue
        # simple diversity: reduce score if body is very similar to already-picked
        penalty = 0.0
        for _, b2, _ in final:
            sim = float(token_set_ratio(body[:200], (b2 or "")[:200])) / 100.0
            if sim > 0.85:
                penalty += 0.1
        final.append((cid, body, max(0.0, score - penalty)))
        seen_ids.add(cid)
    final.sort(key=lambda x: x[2], reverse=True)
    return final[:k]
