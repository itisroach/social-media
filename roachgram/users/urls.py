from django.urls import path
from . import views


urlpatterns = [
    path("" , views.userPage , name="user-page")
]