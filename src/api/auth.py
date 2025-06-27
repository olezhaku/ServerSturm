from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException

from database import check_user
from schemas import UserSchema

from services.jwt import JWTService


router = APIRouter(prefix="/auth")
ph = PasswordHasher()
jwt = JWTService()


@router.post("/tokens")
async def login(creds: UserSchema) -> dict:
    user = await check_user(creds.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    try:
        ph.verify(user.password, creds.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return jwt.create_tokens(creds.username)


@router.post("/tokens/refresh")
async def refresh(token: dict) -> dict:
    tokens = await jwt.refresh_tokens(token["refresh_token"])

    return tokens
