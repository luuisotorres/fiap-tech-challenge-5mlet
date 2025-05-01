from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..auth import (
    create_token,
    authenticate_user
)

router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(credentials: LoginRequest):
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(credentials.username)
    return {"access_token": token}
