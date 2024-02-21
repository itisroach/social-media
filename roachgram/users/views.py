from django.shortcuts import render
from .models import User


def userPage(request , username):
    user = User.objects.get(username = username)
    context = {
        "user": user,
        "htmlTitle": f"{username}'s Page"
    }
    return render(request , "userPage.html" , context)