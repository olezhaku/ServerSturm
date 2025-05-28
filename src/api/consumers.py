import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SimpleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            await self.accept()
            print(f"🟢 WebSocket подключён для {self.scope['user'].username}")
            await self.send(text_data=json.dumps({"message": "Connected!"}))
        else:
            print("❌ Неавторизованный доступ")
            await self.close(code=4000)

    async def disconnect(self, close_code):
        print(f"🔴  WebSocket disconnected: {close_code}")

    async def receive(self, text_data):
        if not self.scope["user"].is_authenticated:
            await self.close(code=4000)
            return
        print(f"🟡 Получено: {text_data}")
        data = json.loads(text_data)
        msg = data.get("message", "")
        if msg.strip() == "/stop":
            print("❌ Клиент отправил /stop")
            await self.close()
            return
        response = {"message": f"You say: {msg}"}
        print(f"🟢 Отправка: {response}")
        await self.send(text_data=json.dumps(response))
