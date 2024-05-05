"""
ASGI config for roachgram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat import routing as chat_routing
from users import routing as notif_routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roachgram.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns+
            notif_routing.websocket_urlpatterns
        )
    )
})


ASGI_APPLICATION = "chat.asgi.application"