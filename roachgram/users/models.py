from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

def user_profile_directory(instance , filename):
    return f"{instance}/{filename}"

class User(AbstractUser):
    email   = models.EmailField()
    about   = models.TextField(max_length=255 , blank=True , null=True)
    profile = models.ImageField(upload_to=user_profile_directory , blank=True , null=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username