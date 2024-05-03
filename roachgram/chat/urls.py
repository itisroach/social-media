from django.urls import path
from . import views

urlpatterns = [
    path("" , views.chat , name="chat-page"),
    path("<str:room_name>" , views.chatRoom , name="chat-room")
]