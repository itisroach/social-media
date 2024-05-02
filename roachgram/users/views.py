from django.db.models.query import QuerySet
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import User , FollowUser
from django.contrib import messages
from .forms import RegisterForm , UpdateUserForm
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from feeds.models import Post , Like , Comment
from django.db.models import Q
def registeration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST , request.FILES)
        if (form.is_valid()):
            registeredUser = form.save()
            login(request , registeredUser)
            
            messages.success(request , "your account created succcessfully")
            return redirect("home-page")
    
    else:
        form = RegisterForm()

    context = {
        "form": form,
        "htmlTitle": "Register New Account"
    }
    return render(request , "register.html" , context)



def userPage(request , username):
    
    try:
        user = User.objects.get(username=username)
        userPosts = Post.objects.filter(Q(user=user) & Q(isReply=False)).order_by("-createdAt")
    except User.DoesNotExist:
        raise Http404



    context = {
        "account": user,
        "posts": userPosts,
        "htmlTitle": f"{username}'s Page"
    }

    return render(request , "userPage.html" , context)

def userPageLikes(request , username):
    try:
        user = User.objects.get(username=username)
        likedPosts = Post.objects.filter(post__in=Like.objects.filter(user=user))[::-1]
    except User.DoesNotExist:
        raise Http404

    

    context = {
        "account": user,
        "posts": likedPosts
    }


    return render(request , "userPage.html" , context)


def userPageReplies(request , username):
    try:
        user = User.objects.get(username=username)
        repliedPosts = Comment.objects.filter(user=user).order_by("-createdAt")

    except User.DoesNotExist:
        raise Http404
    
    context = {
        "account": user,
        "posts": repliedPosts
    }

    return render(request , "userPage.html" , context)

def userFollowers(request , username):
    user = get_object_or_404(User,username=username)
    followers = User.objects.filter(followers__in=FollowUser.objects.filter(following=user))

    context = {
        "users": followers
    }

    return render(request , "followersOrFollowings.html" , context)

def userFollowings(request ,username):
    user = get_object_or_404(User,username=username)
    followings = User.objects.filter(followings__in=FollowUser.objects.filter(follower=user))
    
    context = {
        "users": followings
    }

    return render(request , "followersOrFollowings.html" , context)

@login_required()
def updateUser(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES , instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request , "You Profile Changed Successfullly")
    
    else:
        form = UpdateUserForm(instance=request.user)
    
    return render(request , "profile.html" , { "form": form })

@login_required()
def followUser(request , username):

    # check if user exists in database
    
    try:
        global user
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request , "user not found")
        return redirect("user-page" , username)
    
    if (request.user.id == user.id):
        messages.error(request , "you can't follow yourself")
        return redirect("user-page" , user.username)  
    # checks for user if it's already following
    isFollowing = FollowUser.objects.filter(follower=request.user, following = user).exists()


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


@login_required
def changesPassword(request):
    
    if request.method == "GET":
        return render(request , "changePassword.html")

    user = User.objects.get(username=request.user.username)

    oldPass = request.POST.get("oldPassword")
    newPass = request.POST.get("newPassword")    

    if user.check_password(oldPass):
        user.set_password(newPass)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request , "Your Password Changed Successfully")
        return redirect("update-user")
    
    messages.error(request , "The Old Password Does Not Match")
    return redirect("change-password")


class ResetPassword(PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password-reset-done")