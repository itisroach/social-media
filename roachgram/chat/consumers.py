import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room , Message
from users.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]


        self.roomName = room_name
        await self.channel_layer.group_add(
            self.roomName,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.roomName,
            self.channel_name
        )
    
    # receives anything that sent with send method in client side 
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        message = data["message"]
        username = data["sender"]

        # we use this here because we want messages be saved in database so it will run once not per sockets
        await self.createMessage(username , message)

        # send response to client
        await self.channel_layer.group_send(
            self.roomName,
            {
                'type': "sendMessage",
                "message": message,
                "username": username
            }
        )
    
    # custom event when receive happens
    async def sendMessage(self , event):
        
        
        response = {
            "sender": event["username"],
            "message": event["message"]
        }

        await self.send(json.dumps({"data": response}))

    # creates records at db
    @database_sync_to_async
    def createMessage(self , username , message):
        room = Room.objects.get(name=self.roomName)
        sender = User.objects.get(username=username)
        new_message = Message.objects.create(room=room , message=message, sender=sender)
