from django.db import models
from users.models import User
import os
# Create your models here.

def mediaDirectory(instance , filename):
    return f"{instance.post.user.username}/media/{filename}"

class Post(models.Model):
    user      = models.ForeignKey(User , on_delete=models.CASCADE , related_name="creator")
    caption   = models.TextField(max_length=512)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"posted by {self.user.username}"

    def get_media(self):
        return Media.objects.filter(post = self.id)
    
    def get_like_count(self):
        return Like.objects.filter(post = self).count()

    

    



class Media(models.Model):
    post  = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="post_media")
    file = models.FileField(upload_to=mediaDirectory , blank=True , null=True)


    def __str__(self) -> str:
        return f"{self.file.url}"


    

    def get_type(self):
        videoFormats = [".mp4" , ".mov" , ".avi" , ".wmv" , ".avchd" , ".flv" , ".webm"]
        imageFormats = [".jpg" , ".jpeg" , ".png" , ".gif" , ".tiff" , ".webp"]
        name , extension = os. path.splitext(self.file.url)
        if extension in videoFormats:
            return "video"
        elif extension in imageFormats:
            return "img"


class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="post")


    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.id}"