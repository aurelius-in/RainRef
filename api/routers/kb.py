from fastapi import APIRouter, Query
router = APIRouter()

@router.get("/cards")
def search_cards(query: str = Query(""), tags: str = Query("")):
    return {"results": []}

@router.post("/cards")
def upsert_card(card: dict):
    return {"id": "kb-1", "status": "draft"}
