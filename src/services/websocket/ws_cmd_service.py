import json
from typing import Callable


class WebsocketCommandService:
    def __init__(self, sys_mon: Callable):
        self.sys_mon = sys_mon

    def parse_command(self, data) -> dict:
        data = json.loads(data)

        match data["message"]:
            case "/cpu":
                stats = self.sys_mon()
                formatted = "\n".join(f"*{k}*:  {v}" for k, v in stats.items())
                return formatted
            case "/screen":
                return "CUM"
            case _:
                return "❓ Unknown command"
