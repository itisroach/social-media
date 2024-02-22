from django.contrib.auth.signals import user_logged_out , user_logged_in
from django.dispatch import receiver
from django.contrib import messages


@receiver(user_logged_out)
def userLoggedOut(sender , request , **kwargs):
    messages.success(request , "logged out successfully")


@receiver(user_logged_in)
def userLoggedIn(sender , request , **kwargs):
    messages.success(request , "you were logged in successfully")