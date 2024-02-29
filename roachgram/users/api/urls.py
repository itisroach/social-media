from django.urls import path
from . import viewsets

urlpatterns = [
    path("register" , viewsets.createUser , name="api-create-user")
]