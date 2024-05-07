from django.urls import path
from . import viewsets


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("auth/register/" , viewsets.RegisterUser.as_view() , name="api-register"),    
    path("user" , viewsets.UserView.as_view() , name="api-user"),    
    path("edit-user" , viewsets.UpdateUser.as_view() , name="api-update-user"),
    path("change-password" , viewsets.ChangePassword.as_view() , name="api-change-password"),
    path("users" , viewsets.AllUsers.as_view() , name="all-users"),
    path("users/follow" , viewsets.FollowView.as_view() , name="follow-user"),
    path("users/notifications/" , viewsets.Notifications.as_view() , name="api-notifications"),
    path("users/<str:username>" , viewsets.OneUser.as_view() , name="one-user"),
    path("users/<str:username>/likes" , viewsets.OneUserLikes.as_view() , name="api-user-likes"),
    path("users/<str:username>/replies" , viewsets.OneUserReplies.as_view() , name="api-user-replies"),
    path("users/<str:username>/followers" , viewsets.OneUserFollowers.as_view() , name="api-users-followers"),
    path("users/<str:username>/followings" , viewsets.OneUserFollowings.as_view() , name="api-users-followings"),
    
    # JWT authentication
    path('auth/login', viewsets.MyToken.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),

]