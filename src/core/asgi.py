import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from api.middleware import JwtAuthMiddleware
import api.routing


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JwtAuthMiddleware(URLRouter(api.routing.websocket_urlpatterns))
        ),
    }
)
