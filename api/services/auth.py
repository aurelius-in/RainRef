from fastapi import Header, HTTPException, Depends
from typing import Optional
from config import settings
import time
import jwt
import bcrypt
from sqlalchemy.orm import Session
from models.db import SessionLocal
from models.entities import User


async def require_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    expected = getattr(settings, "api_key", None) or getattr(settings, "API_KEY", None)
    if not expected:
        return  # no key configured -> open
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="invalid api key")


def create_jwt(payload: dict) -> str:
    data = {**payload, "iat": int(time.time()), "exp": int(time.time()) + settings.jwt_exp_minutes * 60}
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")


async def require_admin_jwt(authorization: Optional[str] = Header(None)) -> dict:
    if not settings.require_jwt_for_admin:
        return {}
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]
    claims = verify_jwt(token)
    roles = claims.get("roles") or []
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="admin role required")
    return claims


def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
