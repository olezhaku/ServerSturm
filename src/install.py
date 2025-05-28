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

User = get_user_model()
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "core" / "settings.py"


def generate_random_string(length):
    return secrets.token_urlsafe(length)


def get_ip():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        sys.exit("\n⚠️  Achtung!: NO CONNECTION!\n")


def modify_settings_py(ip, token):
    if not SETTINGS_PATH.exists():
        print("❌ settings.py not found!")
        sys.exit(1)

    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = f.read()

    if "ALLOWED_HOSTS" in settings:
        if ip not in settings:
            settings = settings.replace(
                "ALLOWED_HOSTS = [", f"ALLOWED_HOSTS = [\n    '{ip}',"
            )
    else:
        settings += f"\n\nALLOWED_HOSTS = ['{ip}']"

    # Добавим токен
    if "SUPERUSER_TOKEN" not in settings:
        settings += f"\n\nSUPERUSER_TOKEN = '{token}'"

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        f.write(settings)

    print("🛠️  settings.py updated!\n")


def create_superuser():
    ip = get_ip()
    # ip = "127.0.0.1"
    password = generate_random_string(16)

    if not User.objects.filter(id=1):
        User.objects.create_superuser(username=ip, password=password)

        raw_data = f"{ip}:8000|{password}"
        key = base64.b64encode(raw_data.encode()).decode()

        modify_settings_py(ip, key)

        print("\n✅  Superuser created!")
        print(f"🧾  IP:       {ip}")
        print(f"🔐  Password: {password}\n")
        print(f"🔑  Auth key: SS-KEY-{key}\n")
    else:
        print("⚠️  User is created!")


if __name__ == "__main__":
    call_command("migrate")
    create_superuser()
