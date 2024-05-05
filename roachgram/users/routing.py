from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path("notification/<int:pk>/" , NotificationConsumer.as_asgi())
]
