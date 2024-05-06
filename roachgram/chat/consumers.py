import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room , Message , ConnectionHistory
from users.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user = self.scope["user"]
        
        self.roomName = room_name
        await self.channel_layer.group_add(
            self.roomName,
            self.channel_name
        )
        # update connection history of connected user to True (online)
        dic = await self.update_user_status(username=self.user.username,status=True)
        # runs check_user_status which send data to client to let client know that user is online 
        await self.channel_layer.group_send(
            self.roomName,
            dic
        )
        await self.accept()
        
        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.roomName,
            self.channel_name
        )
        # set user status to offline
        dic = await self.update_user_status(username=self.user.username,status=False)
        # sends data to client to let them know user is offline
        await self.channel_layer.group_send(
            self.roomName,
            dic
        )
            
        
    
    # receives anything that sent with send method in client side 
    async def receive(self, text_data):
        data = json.loads(text_data)
        reqType = data["type"]


        match reqType:
            # chec_user_status
            case "check_user_status":
                # runs a query that gets user's current status
                dic = await self.check_user_status(username=data["username"])
                # sends the result of above code to client
                await self.channel_layer.group_send(
                    self.roomName,
                    dic
                )
            case "message":
                message = data["message"]
                username = self.user.username
                # we use this here because we want messages be saved in database so it will run once not per sockets
                await self.createMessage(message)

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
            "type": "message",
            "sender": event["username"],
            "message": event["message"]
        }

        await self.send(json.dumps(response))

    # send data to client about user status
    async def user_status(self , data):
        response = {
            "type": "user_status",
            "username": data["username"],
            "is_online": data["status"]
        }

        await self.send(json.dumps(response))

    # creates records at db
    @database_sync_to_async
    def createMessage(self , message):
        room = Room.objects.get(name=self.roomName)
        sender = self.user
        Message.objects.create(room=room , message=message, sender=sender)

    # updates user status
    @database_sync_to_async
    def update_user_status(self ,username,  status):
        user = User.objects.get(username=username)
        try:
            ConnectionHistory.objects.get(user=user)
        except ConnectionHistory.DoesNotExist:
            ConnectionHistory.objects.create(user=user)
        
        ConnectionHistory.objects.filter(user=user).update(is_online=status)
        connection = ConnectionHistory.objects.get(user=user)
        dic = {
            "type": "user_status",
            "status": connection.is_online,
            "username": connection.user.username
        }
        return dic
    
    # gets user's current status
    @database_sync_to_async
    def check_user_status(self , username):
        user   = User.objects.get(username=username)
        try:
            status = ConnectionHistory.objects.get(user=user)
        except ConnectionHistory.DoesNotExist:
            status = None
        return {
            "type": "user_status",
            "status": status.is_online if status else False,
            "username": status.user.username if status else username
        }
        