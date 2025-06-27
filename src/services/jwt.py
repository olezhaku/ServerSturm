import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt


class JWTService:
    def __init__(self):
        load_dotenv()

        self.algorithm = os.getenv("JWT_ALGORITHM", "RS256")
        self.access_exp = int(os.getenv("JWT_ACCESS_EXP_MINUTES", 15))
        self.refresh_exp = int(os.getenv("JWT_REFRESH_EXP_DAYS", 7))

        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        keys_dir = os.path.join(base_dir, "keys")

        with open(os.path.join(keys_dir, "private.pem"), "rb") as f:
            self.private_key = f.read()
        with open(os.path.join(keys_dir, "public.pem"), "rb") as f:
            self.public_key = f.read()

    def create_tokens(self, username: str) -> dict:
        now = datetime.now(timezone.utc)
        access_payload = {
            "sub": username,
            "exp": now + timedelta(minutes=self.access_exp),
            "type": "access",
        }
        refresh_payload = {
            "sub": username,
            "exp": now + timedelta(days=self.refresh_exp),
            "type": "refresh",
        }

        return {
            "access": jwt.encode(
                access_payload, self.private_key, algorithm=self.algorithm
            ),
            "refresh": jwt.encode(
                refresh_payload, self.private_key, algorithm=self.algorithm
            ),
        }

    async def verify_token(self, token: str, token_type: str = "access") -> str:
        try:
            payload = jwt.decode(token, self.public_key, algorithms=[self.algorithm])

            if payload.get("type") != token_type or not payload.get("sub"):
                raise HTTPException(401, "Invalid or expired token")

            return payload["sub"]
        except Exception:
            raise HTTPException(401, "Invalid or expired token")

    async def refresh_tokens(self, refresh_token: str) -> dict:
        username = await self.verify_token(refresh_token, "refresh")
        return self.create_tokens(username)
