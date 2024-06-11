"""
ASGI config for stema project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
import app_chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stema.settings')

# application = get_asgi_application()


# Définir votre application ASGI
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(app_chat.routing.websocket_urlpatterns)
    ),
})