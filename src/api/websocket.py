from fastapi import APIRouter, WebSocket

from services.init_services import jwt, ws_cmd_service
from services.websocket.ws_service import WebsocketService

router = APIRouter()


@router.websocket("/sschannel")
async def ws(websocket: WebSocket):
    service = WebsocketService(websocket, jwt, ws_cmd_service)

    if await service.auth():
        await service.connect()
