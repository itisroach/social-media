from django.shortcuts import render , redirect , get_object_or_404
from users.models import User , FollowUser
from django.db.models import Q
from .models import Post , Media , Like , Bookmark
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required()
def home(request):
    feedPosts = Post.objects.filter(
                Q(user=request.user) |
                Q(user__in=FollowUser.objects.filter(
                    follower=request.user
                ).values_list('following'))
                ).order_by("-createdAt")
    context = {
        "feedPosts": feedPosts
    }

    return render(request , "home.html" , context)

@login_required()
def post(request):
    if request.method == "POST":
        # print(request.POST)
        post = Post(user=request.user , caption=request.POST["caption"])
        post.save()
        files = request.FILES.getlist("file")
        for file in files:
            f = Media(post=post , file=file)
            f.save()
        return redirect("home-page")
        


@login_required()
def likePost(request , pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        likedBefore = Like.objects.filter(user=request.user , post=post)

        if likedBefore.exists():
            likedBefore.delete()
        else:
            Like.objects.create(post=post , user=request.user)
    return redirect("home-page")

@login_required()
def bookmarkPost(request , pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        bookmarkedBefore = Bookmark.objects.filter(post=post , user=request.user)

        if bookmarkedBefore.exists():
            bookmarkedBefore.delete()
        else:
            Bookmark.objects.create(user=request.user , post=post)

        return redirect("home-page")