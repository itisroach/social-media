from django.urls import path
from . import viewsets

urlpatterns = [
    path("" , viewsets.PostViews.as_view() ,name="api-posts"),
    path("/<int:pk>" , viewsets.PostDetailView.as_view() , name="api-post-detail")
]