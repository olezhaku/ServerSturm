from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser, User

# TEST
from channels.db import database_sync_to_async


# TEST
@database_sync_to_async
def get_user_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = None
        for param in query_string.split("&"):
            if param.startswith("token="):
                token = param.split("=")[1]
                break

        if token:
            user = await get_user_from_token(token)
            scope["user"] = user
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
