from django.urls import path
from .consumers import NotificationConsumer , SeenNotificationConsumer

websocket_urlpatterns = [
    path("notification/<str:username>/" , NotificationConsumer.as_asgi()),
    path("notification/<str:username>/<int:last_notif_pk>/seen/" , SeenNotificationConsumer.as_asgi())
]
