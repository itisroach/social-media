from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path("@<str:username>" , views.userPage , name="user-page"),
    path("<str:username>/follow/" , views.followUser , name="follow-user"),
    path("<str:username>/unfollow/" , views.unfollowUser , name="unfollow-user"),

    # auth routes
    path("register" , views.registeration , name="register-user"),
    path("login" , authViews.LoginView.as_view(template_name="login.html" , redirect_authenticated_user=True) , name="login-user"),
    path("logout" , authViews.LogoutView.as_view() , name="logout-user")
]