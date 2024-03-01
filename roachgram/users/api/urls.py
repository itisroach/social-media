from django.urls import path
from . import viewsets


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register" , viewsets.createUser , name="api-create-user"),    
    path("edit-user" , viewsets.UpdateUser.as_view() , name="api-update-user"),
    path("change-password" , viewsets.ChangePassword.as_view() , name="api-change-password"),
    path("users" , viewsets.AllUsers.as_view() , name="all-users"),
    path("users/<str:username>" , viewsets.OneUser.as_view() , name="one-user"),
    # JWT authentication
    path('token/', viewsets.MyToken.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]