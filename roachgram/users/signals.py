from django.contrib.auth.signals import user_logged_out , user_logged_in
from django.db.models.signals import pre_delete , pre_save
from django.dispatch import receiver
from django.contrib import messages
from .models import User
# for removing folders and files
import shutil
import os

from roachgram.settings import BASE_DIR

# shows a message when user is logged out
@receiver(user_logged_out)
def userLoggedOut(sender , request , **kwargs):
    messages.success(request , "logged out successfully")

# shows a message when user is logged in
@receiver(user_logged_in)
def userLoggedIn(sender , request , **kwargs):
    messages.success(request , "you were logged in successfully")

# removes a folder
def removeDir(path):
    fileLocation = os.path.join(BASE_DIR, path)
    shutil.rmtree(fileLocation , ignore_errors=False)

# when user account deleted all of its uploads gets deleted
@receiver(pre_delete , sender=User)
def on_user_delete(sender , instance , **kwargs):
    removeDir(f"uploads/{instance.username}")


def deleteFile(path):
    # checks if path is a file
    if os.path.isfile(path):
        os.remove(path)


# when user model is updated removes the previous profile picture
@receiver(pre_save , sender=User)
def on_profile_change(sender , instance , **kwargs):
    # if the instance does not exist creates one
    if instance.id is None:
        pass
    else:
        
        # get the previous user object
        previous = User.objects.get(id=instance.id)
        print(previous.profile)
        # checks if profile field is changed or not
        if previous.profile != instance.profile and previous.profile != "default-profile.png":
            deleteFile(f"uploads/{previous.profile}")