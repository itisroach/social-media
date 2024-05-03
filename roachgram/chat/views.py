from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import FollowUser

@login_required
def chat(request):
    followedUsers = FollowUser.objects.filter(follower=request.user)
    
    context = {
        "available_users_to_chat": followedUsers
    }

    return render(request , "chatPage.html" , context)