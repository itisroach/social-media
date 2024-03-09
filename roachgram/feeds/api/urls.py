from django.urls import path
from . import viewsets

urlpatterns = [
    path("" , viewsets.PostViews.as_view() ,name="api-posts"),
    path("<int:pk>" , viewsets.PostDetailView.as_view() , name="api-post-detail"),
    path("<int:pk>/comments" , viewsets.CommentView.as_view() , name="api-comment"),
    path("users/<str:username>" , viewsets.UserPostListView.as_view() , name="api-user-post"),
    path("like" , viewsets.LikePostView.as_view() , name="api-like-post"),
    path("bookmark" , viewsets.BoookmarkView.as_view() , name="api-bookmark-post")
]