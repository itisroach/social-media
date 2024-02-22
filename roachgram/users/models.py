from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

def user_profile_directory(instance , filename):
    return f"{instance}/{filename}"

class User(AbstractUser):
    name    = models.CharField(max_length=255 , blank=True , null=True)
    email   = models.EmailField()
    about   = models.TextField(max_length=255 , blank=True , null=True)
    profile = models.ImageField(upload_to=user_profile_directory , default="default-profile.png" , blank=True , null=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    

class FollowUser(models.Model):
    follower = models.ForeignKey(User , on_delete=models.CASCADE , related_name="followers")
    following = models.ForeignKey(User , on_delete=models.CASCADE , related_name="followings")
    createdAt = models.TimeField(auto_now_add=True , blank=True , null=True)
    updatedAt = models.TimeField(auto_now=True , blank=True , null=True)


    def __str__(self):
        return f"{self.follower.username} following {self.following.username}"