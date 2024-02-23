from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post
import os
# import delete file function from users app signals
from users.signals import deleteFile


# before post gets deleted removes the media of it
@receiver(pre_delete , sender=Post)
def on_post_remove(sender , instance , **kwargs):
    # check if image is exists
    allMedia = instance.get_media()
    if (len(allMedia) > 0):
        for media in allMedia:
            # first change Media type to string and then removes first slash to path be recognized to os.remove
            deleteFile(str(media).replace("/" , "" , 1))

    
    
    