from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def user_profile_directory(instance):
    return f"uploads/{instance.id}"

class User(AbstractUser):
    email   = models.EmailField()
    about   = models.TextField(max_length=255)
    profile = models.ImageField(upload_to=user_profile_directory)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username