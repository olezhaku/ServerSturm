from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from services.jwt import JWTService
from services.websocket.ws_cmd_service import WebsocketCommandService


class WebsocketService:
    def __init__(
        self,
        websocket: WebSocket,
        jwt: JWTService,
        ws_cmd: WebsocketCommandService,
    ):
        self.ws = websocket
        self.jwt = jwt
        self.ws_cmd = ws_cmd

    async def auth(self) -> bool:
        token = self.ws.query_params.get("token")

        if not token:
            await self.ws.close(code=1008)
            return False

        try:
            await self.jwt.verify_token(token)
            return True
        except HTTPException:
            await self.ws.close(code=1008)
            return False

    async def connect(self) -> None:
        await self.ws.accept()

        try:
            while True:
                data = await self.ws.receive_text()
                result = self.ws_cmd.parse_command(data)

                await self.ws.send_text(result)
        except WebSocketDisconnect:
            print("websocket disconnected")
