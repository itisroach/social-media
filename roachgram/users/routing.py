from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path("notification/<str:username>/" , NotificationConsumer.as_asgi())
]
