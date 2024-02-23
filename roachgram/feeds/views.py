from django.shortcuts import render
from users.models import User , FollowUser
from .models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required()
def home(request):
    feedPosts = Post.objects.filter(
                user__in=FollowUser.objects.filter(
                    follower=request.user
                ).values_list('following')
                ).order_by("-createdAt")
    context = {
        "feedPosts": feedPosts
    }

    return render(request , "home.html" , context)