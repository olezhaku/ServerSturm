import asyncio
import os
import sys
import secrets
from argon2 import PasswordHasher
from dotenv import load_dotenv
import requests
import base64

from database import async_main, have_users, create_user
from schemas import UserSchema


load_dotenv()

ph = PasswordHasher()
LOCAL = os.getenv("LOCAL", "False").lower() == "true"


print("\n\n|-| |-| ⚡️ ••• Zip File! ••• ⚡️ |-| |-|\n")

# CORS
# def modify_cors(ip):
#     with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
#         settings = f.read()

#     settings = settings.replace("ALLOWED_HOSTS = [", f"ALLOWED_HOSTS = ['{ip}'")

#     with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
#         f.write(settings)

#     print("🛠️   settings.py updated!\n")


def get_ip() -> str:
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        sys.exit("\n⚠️  Achtung!: NO CONNECTION!\n")


async def create() -> None:
    user = await have_users()
    ip = "127.0.0.1" if LOCAL else get_ip()
    password = secrets.token_urlsafe(16)

    # modify_cors(ip)

    if not user:
        hashed_password = ph.hash(password)
        creds = UserSchema(username=ip, password=hashed_password)

        await create_user(creds)

        raw_data = f"{ip}:8000|{password}"
        sskey = base64.b64encode(raw_data.encode()).decode()

        print("\n✅  Superuser created!")
        print(f"🧾  IP:       {ip}")
        print(f"🔐  Password: {password}\n")
        print(f"🔑  Auth key: SS-KEY-{sskey}\n")
    else:
        print("⚠️  User is created!")


if __name__ == "__main__":
    asyncio.run(async_main())
    asyncio.run(create())
