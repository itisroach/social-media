from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import User , FollowUser
from django.contrib import messages



def userPage(request , username):
    user = User.objects.get(username = username)

    # make this statement login required
    if request.user.is_authenticated:
        # checks for user if it's following 
        global isFollowing
        isFollowing = FollowUser.objects.filter(follower=request.user, following = user).exists()


    context = {
        "account": user,
        "htmlTitle": f"{username}'s Page",
        "isFollowingTheUser": isFollowing
    }

    return render(request , "userPage.html" , context)

@login_required()
def followUser(request , username):

    # check if user exists in database
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request , "user not found")
        return redirect("user-page" , "reza")
    

    # checks for user if it's already following
    isFollowing = FollowUser.objects.filter(follower=request.user, following = user).exists()

    print(isFollowing)

    if (isFollowing):
        messages.error(request , f"you already following @{user.username}")
        return redirect("user-page" , user.username)

    # if user not following already it creats a record in database
    FollowUser.objects.create(follower=request.user , following=user)
    messages.success(request , f"you are now following @{user.username}")
    return redirect("user-page" , user.username)


@login_required()
def unfollowUser(request , username):

    # check if user exists in database
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request , "user not found")
        return redirect("user-page" , "reza")
    

    # checks for user if it's already following
    isFollowing = FollowUser.objects.filter(follower=request.user, following = user).exists()


    if (not isFollowing):
        messages.error(request , f"you'r not following @{user.username} so you can't unfollow")
        return redirect("user-page" , user.username)

    # if user not following already it creats a record in database
    FollowUser.objects.get(follower=request.user , following=user).delete()
    messages.success(request , f"you are now not following @{user.username}")
    return redirect("user-page" , user.username)