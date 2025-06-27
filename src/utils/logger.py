import json
from datetime import datetime


class ASGILoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = datetime.utcnow().isoformat()

        # Логируем только WebSocket и HTTP
        if scope["type"] in ["websocket", "http"]:
            log = {
                "time": start_time,
                "type": scope["type"],
                "method": scope.get("method"),
                "path": scope.get("path"),
                "query_string": scope.get("query_string").decode("utf-8"),
                "headers": {
                    k.decode(): v.decode() for k, v in scope.get("headers", [])
                },
                "client": scope.get("client"),
                "server": scope.get("server"),
            }

            print("\n🟡 ASGI Middleware intercepted:\n" + json.dumps(log, indent=2))

        async def custom_send(message):
            # Ловим попытки отклонения WebSocket
            if message["type"] == "websocket.close":
                print(f"🔴 WebSocket closed with code: {message.get('code')}")
            elif message["type"] == "websocket.accept":
                print("🟢 WebSocket accepted")
            elif message["type"] == "websocket.send":
                print(f"📝 Sent to WS: {message.get('text')}")
            elif message["type"] == "http.response.start":
                print(f"📤 HTTP status: {message['status']}")

            await send(message)

        await self.app(scope, receive, custom_send)
