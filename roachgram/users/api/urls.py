from django.urls import path
from . import viewsets


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register" , viewsets.RegisterUser.as_view() , name="api-register"),    
    path("user" , viewsets.UserView.as_view() , name="api-user"),    
    path("edit-user" , viewsets.UpdateUser.as_view() , name="api-update-user"),
    path("change-password" , viewsets.ChangePassword.as_view() , name="api-change-password"),
    path("users" , viewsets.AllUsers.as_view() , name="all-users"),
    path("users/follow" , viewsets.FollowView.as_view() , name="follow-user"),
    path("users/<str:username>" , viewsets.OneUser.as_view() , name="one-user"),
    path("users/<str:username>/followers" , viewsets.OneUserFollowers.as_view() , name="api-users-followers"),
    path("users/<str:username>/followings" , viewsets.OneUserFollowings.as_view() , name="api-users-followings"),
    
    # JWT authentication
    path('login', viewsets.MyToken.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]