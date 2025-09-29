from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from services.auth import create_jwt, verify_jwt


class LoginIn(BaseModel):
    username: str
    password: str


router = APIRouter()


@router.post("/login")
def login(body: LoginIn):
    # Simple fixed admin for now; replaced by DB lookup later
    if body.username == "admin" and body.password == "admin":
        token = create_jwt({"sub": body.username, "roles": ["admin"]})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="invalid credentials")


@router.get("/whoami")
def whoami(authorization: str | None = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        return {"user": "anonymous"}
    token = authorization.split(" ", 1)[1]
    claims = verify_jwt(token)
    return {"user": claims.get("sub"), "roles": claims.get("roles", [])}


