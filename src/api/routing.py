from django.urls import re_path
from . import consumers

websocket_urlpatterns = [re_path(r"sschannel/$", consumers.SimpleConsumer.as_asgi())]
