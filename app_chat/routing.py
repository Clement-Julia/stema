# routing.py
from django.urls import path
from django.urls import re_path
from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     path("ws/chat/<int:conversation_id>/", ChatConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>\w+)/$', ChatConsumer.as_asgi()),
]