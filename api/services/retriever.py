from sqlalchemy.orm import Session
from sqlalchemy import select, text
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
    """Hybrid retrieval using Postgres FTS candidates + vector rerank, with RapidFuzz fallback.

    Returns list of (card_id, body, score).
    """
    candidates: List[Tuple[str, str, float]] = []

    # Prepare embedding for semantic scoring
    from .kb_embed import embed_text
    qv = embed_text(query or "")

    # Stage 1: get candidates via Postgres FTS if possible
    try:
        if (query or "").strip():
            # Use plainto_tsquery for safer parsing
            limit = max(k * 5, 20)
            sql = text(
                """
                SELECT id, title, body, embedding,
                       ts_rank(tsv, plainto_tsquery('english', :q)) AS fts
                FROM kb_cards
                WHERE tsv @@ plainto_tsquery('english', :q)
                ORDER BY fts DESC
                LIMIT :limit
                """
            )
            rows = db.execute(sql.bindparams(q=query, limit=limit)).all()
            for rid, title, body, emb, fts in rows:
                text_blob = (title or "") + "\n" + (body or "")
                # lexical score from ts_rank (typically 0..1+); normalize roughly
                lex_score = float(fts or 0.0)
                # convert to ~0..1 range
                lex_score = max(0.0, min(1.0, lex_score))
                vecsim = cosine(qv, (emb or [])[:len(qv)])
                hybrid = 0.6 * lex_score + 0.4 * vecsim
                candidates.append((rid, body or "", hybrid))
        else:
            # No query -> take recent cards via ORM (select only needed columns)
            rows = db.execute(select(KbCard.id, KbCard.title, KbCard.body, KbCard.embedding).limit(max(k * 5, 20))).all()
            for rid, title, body, emb in rows:
                text_blob = (title or "") + "\n" + (body or "")
                bm25ish = float(token_set_ratio((query or ""), text_blob))
                lex_score = bm25ish / 100.0
                vecsim = cosine(qv, (emb or [])[:len(qv)])
                hybrid = 0.6 * lex_score + 0.4 * vecsim
                candidates.append((rid, body or "", hybrid))
    except Exception:
        # Ensure session is usable after SQL error
        try:
            db.rollback()
        except Exception:
            pass
        # Fallback: in-Python lexical + vector over all rows
        rows = db.execute(select(KbCard.id, KbCard.title, KbCard.body, KbCard.embedding)).all()
        for rid, title, body, emb in rows:
            text_blob = (title or "") + "\n" + (body or "")
            bm25ish = float(token_set_ratio((query or ""), text_blob))
            lex_score = bm25ish / 100.0
            vecsim = cosine(qv, (emb or [])[:len(qv)])
            hybrid = 0.6 * lex_score + 0.4 * vecsim
            candidates.append((rid, body or "", hybrid))

    # If FTS returned nothing, do a broad lexical+vector sweep as fallback
    if not candidates:
        try:
            rows = db.execute(select(KbCard.id, KbCard.title, KbCard.body, KbCard.embedding)).all()
            for rid, title, body, emb in rows:
                text_blob = (title or "") + "\n" + (body or "")
                bm25ish = float(token_set_ratio((query or ""), text_blob))
                lex_score = bm25ish / 100.0
                vecsim = cosine(qv, (emb or [])[:len(qv)])
                hybrid = 0.6 * lex_score + 0.4 * vecsim
                if hybrid > 0:
                    candidates.append((rid, body or "", hybrid))
        except Exception:
            pass

    # Rerank and diversify
    buffer = max(k * 5, 10)
    candidates.sort(key=lambda x: x[2], reverse=True)
    top = candidates[:buffer]
    final: List[Tuple[str, str, float]] = []
    for cid, body, score in top:
        # light diversity: penalize if very similar to already selected bodies
        penalty = 0.0
        for _, b2, _ in final:
            sim = float(token_set_ratio((body or "")[:200], (b2 or "")[:200])) / 100.0
            if sim > 0.85:
                penalty += 0.1
        final.append((cid, body, max(0.0, score - penalty)))
    final.sort(key=lambda x: x[2], reverse=True)
    return final[:k]
