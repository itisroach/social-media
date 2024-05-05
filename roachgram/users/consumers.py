import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # gets user id from url
        self.roomName = self.scope["url_route"]["kwargs"]["pk"]
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.roomName,
            self.channel_name
        )

        await self.accept()