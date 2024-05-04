from django.db import models
from users.models import User

class Room(models.Model):
    name = models.CharField(max_length=256)
    sender = models.ForeignKey(User , on_delete=models.CASCADE , null=False , related_name="sender")
    receiver = models.ForeignKey(User , on_delete=models.CASCADE , null=False , related_name="receiver")

    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(Room , on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User , on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.sender.username} sent to {self.room.name}'
    

class ConnectionHistory(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} is {'Online' if self.is_online else 'Offline'}"