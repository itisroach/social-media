from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("@<str:username>" , views.userPage , name="user-page"),
    path("<str:username>/follow/" , views.followUser , name="follow-user"),
    path("<str:username>/unfollow/" , views.unfollowUser , name="unfollow-user")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)