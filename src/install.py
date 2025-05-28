import sys
import os
import secrets
import requests
import base64

import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

User = get_user_model()


def generate_random_string(length):
    return secrets.token_urlsafe(length)


def get_ip():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        sys.exit("\n⚠️  Achtung!: NO CONNECTION!\n")


def create_superuser():
    # ip = get_ip()
    ip = "127.0.0.1"
    password = generate_random_string(16)

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
    call_command("migrate")
    create_superuser()
