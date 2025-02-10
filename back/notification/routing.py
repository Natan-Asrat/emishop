from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('emishop/ws/chat/<conversation_id>', consumers.ChatConsumer.as_asgi()),
    path('emishop/ws/notifications/<user_id>', consumers.NotificationConsumer.as_asgi())
]
