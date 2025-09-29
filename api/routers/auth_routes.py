from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from services.auth import create_jwt, verify_jwt, get_db, verify_password
from sqlalchemy.orm import Session
from models.entities import User


class LoginIn(BaseModel):
    username: str
    password: str


router = APIRouter()


@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    email = body.username.lower().strip()
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_jwt({"sub": user.email, "roles": user.roles or []})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/whoami")
def whoami(authorization: str | None = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        return {"user": "anonymous"}
    token = authorization.split(" ", 1)[1]
    claims = verify_jwt(token)
    return {"user": claims.get("sub"), "roles": claims.get("roles", [])}


