import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification , NotificationType
from channels.db import database_sync_to_async
from users.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # gets user id from url
        self.username = self.scope["url_route"]["kwargs"]["username"]
        # gets logged in user
        self.user = self.scope["user"]

        # creates new websocket
        await self.channel_layer.group_add(
            self.username,
            self.channel_name
        )

        await self.accept()

        

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.username,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        reqType = data["type"]
        match reqType:
            case "check_notifs":
                new_notif_count_dic = await self.check_unread_notification()
                await self.channel_layer.group_send(
                    self.username,
                    new_notif_count_dic
                )
            case _:
                # creates record in DB
                new_notif_dic = await self.createNotificationInDB(reqType , data["user_to_notif"])

                # sends an json to user is notif is about to send
                await self.channel_layer.group_send(
                    data["user_to_notif"],
                    new_notif_dic
                )
            
                
    
    async def sendResponse(self , event):
        response = {
            "message": event["message"]
        }

        await self.send(json.dumps(response))

    async def sendCheckResponse(self , event):
        response = {
            "notif_count": event["notif_count"]
        }

        await self.send(json.dumps(response))

    @database_sync_to_async
    def createNotificationInDB(self , type: str , username):
        notifType = NotificationType.objects.get(type=type.upper())
        userToNotif = User.objects.get(username=username)
        newNotif = Notification.objects.create(notif_type=notifType , user_to_notif=userToNotif , triggered_by=self.user)
        return {
            "type": "sendResponse",
            "message": f'{self.user.username} {newNotif.notif_type.text}' 
        }
    
    @database_sync_to_async
    def check_unread_notification(self):
        newNotifCount = Notification.objects.filter(user_to_notif=self.user , seen=False).count()
        return {
            "type": "sendCheckResponse",
            "notif_count": newNotifCount
        }


class SeenNotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.last_notification_id = self.scope["url_route"]["kwargs"]["last_notif_pk"]
        self.username = self.scope["url_route"]["kwargs"]["username"]

        await self.channel_layer.group_add(
            f'{self.user.id}{self.user.username}',
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f'{self.user.id}{self.user.username}',
            self.channel_name
        )

    async def receive(self, text_data):

        await self.mark_seen_notifications()
        
    

    @database_sync_to_async
    def mark_seen_notifications(self):
        Notification.objects.filter(user_to_notif=self.user , seen=False).update(seen=True)
