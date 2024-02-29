from django.db import models
from django.contrib.auth.models import AbstractUser
import auto_prefetch
# Create your models here.

def user_profile_directory(instance , filename):
    return f"{instance}/{filename}"

class User(AbstractUser):
    name    = models.CharField(max_length=255 , blank=True , null=True)
    email   = models.EmailField(unique=True)
    about   = models.TextField(max_length=255 , blank=True , null=True)
    profile = models.ImageField(upload_to=user_profile_directory , default="default-profile.png" , blank=True , null=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    
    def get_followers_and_followings_count(self):
        followersCount = FollowUser.objects.filter(following=self).count()
        followingsCount = FollowUser.objects.filter(follower=self).count()

        return {
            "followersCount": followersCount,
            "followingsCount": followingsCount
        }
    
    def get_all_user_posts(self):
        from feeds.models import Post  
        return Post.objects.filter(user=self).order_by("-createdAt")
    
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

class FollowUser(models.Model):
    follower = auto_prefetch.ForeignKey(User , on_delete=models.CASCADE , related_name="followers")
    following = auto_prefetch.ForeignKey(User , on_delete=models.CASCADE , related_name="followings")
    createdAt = models.TimeField(auto_now_add=True , blank=True , null=True)
    updatedAt = models.TimeField(auto_now=True , blank=True , null=True)


    def __str__(self):
        return f"{self.follower.username} following {self.following.username}"