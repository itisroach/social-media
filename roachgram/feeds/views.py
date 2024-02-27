from typing import Any
from django.db.models.query import QuerySet
from django.contrib import messages
from django.shortcuts import render , redirect , get_object_or_404
from users.models import User , FollowUser
from django.db.models import Q
from .models import Post , Media , Like , Bookmark , Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from bleach import clean
# Create your views here.
@login_required()
def home(request):
    condition1 = Q(user=request.user)
    condition2 = Q(post__in=FollowUser.objects.filter(follower=request.user).values_list('following'))
    condition3 = Q(isReply=False)
    feedPosts = Post.objects.filter((condition1 | condition2) & condition3).order_by("-createdAt")
    context = {
        "feedPosts": feedPosts
    }

    return render(request , "home.html" , context)

@require_http_methods(["POST"])
@login_required()
def post(request):
    # print(request.POST)
    post = Post(user=request.user , caption=clean(request.POST["caption"]))
    post.save()
    files = request.FILES.getlist("file")
    for file in files:
        f = Media(post=post , file=file)
        f.save()
    return redirect("home-page")
        
@require_http_methods(["POST"])
def comment(request , pk):
    post = Post.objects.get(id=pk)

    if post is None:
        messages.error(request , "Post Not Found")
        return redirect("home-page")

    comment = Comment.objects.create(repliedTo=post , user=request.user , caption=clean(request.POST["caption"]), isReply=True)

    files = request.FILES.getlist("file")

    for file in files:
        f = Media.objects.create(post=comment , file=file)
    return redirect('single-post-page' , post.id)

@require_http_methods(["GET"])
def singlePost(request , pk):
    post = Post.objects.get(id=pk)

    if post is None:
        messages.error(request , "Post Not Found")
        return redirect("home-page")
    
    comments = post.post_replied_to.all()

    context = {
        "post": post,
        "comments": comments
    }

    return render(request , "singlePost.html" , context)

@login_required()
def likePost(request , pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        likedBefore = Like.objects.filter(user=request.user , post=post)

        if likedBefore.exists():
            likedBefore.delete()
        else:
            Like.objects.create(post=post , user=request.user)
    return redirect("single-post-page" , post.id)

@require_http_methods(["POST"])
@login_required()
def bookmarkPost(request , pk):
    post = Post.objects.get(id=pk)


    bookmarkedBefore = Bookmark.objects.filter(post=post , user=request.user)

    if bookmarkedBefore.exists():
        bookmarkedBefore.delete()
    else:
        Bookmark.objects.create(user=request.user , post=post)

    return redirect("bookmark-page")
    

class GetAllBookmarks(LoginRequiredMixin , ListView):
    model = Bookmark
    context_object_name = "bookmarks"
    template_name = "bookmark.html"
    def get_queryset(self) -> QuerySet[Any]:
        return Bookmark.objects.filter(user=self.request.user).order_by("-createdAt")
    

@require_http_methods(["POST"])
def deletePost(request , pk):
    post = Post.objects.get(id=pk)
    
    if post.user.id != request.user.id:
        messages.error(request , "You Can Not Delete Someone Else's Post")
        return redirect("home-page")
    
    post.delete()
    messages.success(request , "Post Deleted Successfully")
    return redirect("home-page")
