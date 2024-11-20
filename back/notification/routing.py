from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/chat/<conversation_id>', consumers.ChatConsumer.as_asgi())
]