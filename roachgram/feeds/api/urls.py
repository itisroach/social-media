from django.urls import path
from . import viewsets

urlpatterns = [
    path("" , viewsets.PostViews.as_view() ,name="api-posts"),
    path("<int:pk>" , viewsets.PostDetailView.as_view() , name="api-post-detail"),
    path("users/<str:username>" , viewsets.UserPostListView.as_view() , name="api-user-post"),
    path("like" , viewsets.LikePostView.as_view() , name="api-like-post")
]