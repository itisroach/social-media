from django.db import models
from users.models import User
# Create your models here.

def mediaDirectory(instance , filename):
    return f"{instance.user.username}/media/{filename}"

class Post(models.Model):
    user      = models.ForeignKey(User , on_delete=models.CASCADE , related_name="creator")
    image     = models.ImageField(upload_to=mediaDirectory , blank=True , null=True)
    video     = models.FileField(upload_to=mediaDirectory , blank=True , null=True)
    caption   = models.TextField(max_length=512)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="post")