from services.jwt import JWTService
from services.websocket.ws_cmd_service import WebsocketCommandService
from system.sys_mon import sys_mon


jwt = JWTService()
ws_cmd_service = WebsocketCommandService(sys_mon=sys_mon)
