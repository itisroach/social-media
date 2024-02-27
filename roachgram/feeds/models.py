from django.db import models
from users.models import User
import os
import auto_prefetch
# Create your models here.

def mediaDirectory(instance , filename):
    return f"{instance.post.user.username}/media/{filename}"

class Post(models.Model):
    user      = auto_prefetch.ForeignKey(User , on_delete=models.CASCADE , related_name="creator")
    caption   = models.TextField(max_length=512)
    isReply   = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"posted by {self.user.username}"

    def get_media(self):
        return Media.objects.filter(post = self.id)
    

    def get_like_count(self):
        return self.post.count()
    
    def get_comments_count(self):
        return self.post_replied_to.count()

    def get_bookmark_count(self):
        return self.bookmark_set.count()
    
    

    



class Media(models.Model):
    post  = auto_prefetch.ForeignKey(Post , on_delete=models.CASCADE , related_name="post_media")
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
    user = auto_prefetch.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    post = auto_prefetch.ForeignKey(Post , on_delete=models.CASCADE , related_name="post")

    createdAt = models.TimeField(auto_now_add=True)
    updatedAt = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.id}"
    



class Bookmark(models.Model):
    user = auto_prefetch.ForeignKey(User , on_delete=models.CASCADE)
    post = auto_prefetch.ForeignKey(Post , on_delete=models.CASCADE)

    createdAt = models.TimeField(auto_now_add=True)
    updatedAt = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.post.id} saved by {self.user.username}"
    


class Comment(Post , models.Model):
    repliedTo = auto_prefetch.ForeignKey(Post , on_delete=models.CASCADE , related_name="post_replied_to")