from sqlalchemy.orm import Session
from typing import List, Tuple
from .retriever import retrieve

def retrieve_with_citations(db: Session, query: str, k: int = 3) -> List[Tuple[str, str]]:
    hits = retrieve(db, query, k)
    return [(cid, body) for cid, body, _ in hits]

def compose_answer(query: str, citations: List[Tuple[str, str]]) -> str:
    bullet_lines = [f"- [kb:{cid}]" for cid, _ in citations]
    body = "\n".join(bullet_lines) or ""
    return f"We looked into this. Here are helpful sources to resolve it.\n\n{body}"
