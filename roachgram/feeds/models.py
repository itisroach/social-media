from django.db import models
from users.models import User
# Create your models here.

def mediaDirectory(instance , filename):
    return f"{instance.post.user.username}/media/{filename}"

class Post(models.Model):
    user      = models.ForeignKey(User , on_delete=models.CASCADE , related_name="creator")
    caption   = models.TextField(max_length=512)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def get_media(self):
        return Media.objects.filter(post = self.id)



class Media(models.Model):
    post  = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="post_media")
    file = models.FileField(upload_to=mediaDirectory , blank=True , null=True)


    def __str__(self) -> str:
        return f"{self.file.url}"

class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="post")