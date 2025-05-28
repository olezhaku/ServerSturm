import sys
import os
import secrets
import requests
import base64

import django
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management import call_command


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "core" / "settings.py"
User = get_user_model()


def create_env():
    env_vars = {}

    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    if "SECRET_KEY" not in env_vars or not env_vars["SECRET_KEY"]:
        env_vars["SECRET_KEY"] = secrets.token_urlsafe(38)

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    print(f"✅ .env updated at {ENV_PATH}\n")


def modify_settings_py(ip):
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = f.read()

    if "ALLOWED_HOSTS" in settings:
        if ip not in settings:
            settings = settings.replace(
                "ALLOWED_HOSTS = [", f"ALLOWED_HOSTS = [\n    '{ip}',"
            )
    else:
        settings += f"\n\nALLOWED_HOSTS = ['{ip}']"

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        f.write(settings)

    print("🛠️  settings.py updated!\n")


def get_ip():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        sys.exit("\n⚠️  Achtung!: NO CONNECTION!\n")


def create_superuser():
    ip = get_ip()
    # ip = "127.0.0.1"
    password = secrets.token_urlsafe(16)

    if not User.objects.filter(id=1):
        User.objects.create_superuser(username=ip, password=password)

        raw_data = f"{ip}:8000|{password}"
        key = base64.b64encode(raw_data.encode()).decode()

        print("\n✅  Superuser created!")
        print(f"🧾  IP:       {ip}")
        print(f"🔐  Password: {password}\n")
        print(f"🔑  Auth key: SS-KEY-{key}\n")
    else:
        print("⚠️  User is created!")


if __name__ == "__main__":
    create_env()
    call_command("migrate")
    create_superuser()
