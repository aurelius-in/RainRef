from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.adapters import get_adapter
from services.auth import require_admin_jwt


class AdapterTestIn(BaseModel):
    name: str
    payload: dict


router = APIRouter()


@router.post("/test")
def adapter_test(body: AdapterTestIn, _: dict = Depends(require_admin_jwt)):
    ad = get_adapter((body.name or "").lower())
    if not ad:
        raise HTTPException(status_code=404, detail="adapter_not_found")
    try:
        rid = ad.perform(body.payload or {})
        return {"ok": True, "result": rid}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


