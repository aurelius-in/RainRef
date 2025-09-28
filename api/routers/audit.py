from fastapi import APIRouter
router = APIRouter()

@router.get("/{receipt_id}")
def get_receipt(receipt_id: str):
    return {"receipt_id": receipt_id, "verified": True}
