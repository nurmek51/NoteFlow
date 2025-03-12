from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Public chat
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # Private chat
    re_path(r'^ws/private/(?P<room_name>[\w-]+)/$', consumers.PrivateChatConsumer.as_asgi()),
]
