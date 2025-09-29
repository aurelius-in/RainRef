from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import os
import json
from services.auth import require_admin_jwt


CFG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "adapters.json")


class AdapterConfig(BaseModel):
    zendesk_base_url: Optional[str] = None
    zendesk_token: Optional[str] = None
    intercom_base_url: Optional[str] = None
    intercom_token: Optional[str] = None
    github_repo: Optional[str] = None
    github_token: Optional[str] = None


router = APIRouter()


def _ensure_dir(path: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)


@router.get("/adapters/config")
def get_adapters_config(_: dict = Depends(require_admin_jwt)):
    try:
        if os.path.exists(CFG_PATH):
            with open(CFG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        else:
            cfg = {}
    except Exception:
        cfg = {}
    # Prefer env over file
    cfg_out = {
        "zendesk_base_url": os.getenv("ZENDESK_BASE_URL", cfg.get("zendesk_base_url")),
        "zendesk_token": "****" if (os.getenv("ZENDESK_TOKEN") or cfg.get("zendesk_token")) else None,
        "intercom_base_url": os.getenv("INTERCOM_BASE_URL", cfg.get("intercom_base_url")),
        "intercom_token": "****" if (os.getenv("INTERCOM_TOKEN") or cfg.get("intercom_token")) else None,
        "github_repo": os.getenv("GITHUB_REPO", cfg.get("github_repo")),
        "github_token": "****" if (os.getenv("GITHUB_TOKEN") or cfg.get("github_token")) else None,
    }
    return cfg_out


@router.post("/adapters/config")
def save_adapters_config(body: AdapterConfig, _: dict = Depends(require_admin_jwt)):
    # Persist to file; note that env vars won't survive process restarts
    try:
        _ensure_dir(CFG_PATH)
        existing = {}
        if os.path.exists(CFG_PATH):
            with open(CFG_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        data = existing.copy()
        for k, v in body.model_dump(exclude_none=True).items():
            data[k] = v
            # Also set process env for immediate effect
            env_map = {
                "zendesk_base_url": "ZENDESK_BASE_URL",
                "zendesk_token": "ZENDESK_TOKEN",
                "intercom_base_url": "INTERCOM_BASE_URL",
                "intercom_token": "INTERCOM_TOKEN",
                "github_repo": "GITHUB_REPO",
                "github_token": "GITHUB_TOKEN",
            }
            env_key = env_map.get(k)
            if env_key and v is not None:
                os.environ[env_key] = str(v)
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


