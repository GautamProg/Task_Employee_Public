import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmployeeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("employees", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("employees", self.channel_name)

    async def send_update(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))






class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("login_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("login_updates", self.channel_name)

    async def send_login_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))
