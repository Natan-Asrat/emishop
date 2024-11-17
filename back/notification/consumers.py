from channels.generic.websocket import WebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.user_id = self.user.get("user_id", None)
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_id, self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.conversation_id, self.channel_name)
        super().disconnect(close_code)
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        reservation_id = data.get('reservation_id')
        if reservation_id:
            message = Message.objects.create(
                sender_id = self.user_id,
                conversation_id = self.conversation_id,
                content = data.get('message'),
                reservation_id = reservation_id
            )
        else:
            message = Message.objects.create(
                sender_id = self.user_id,
                conversation_id = self.conversation_id,
                content = data.get('message')
            )
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_id,
            {
                'type': 'chat_message',
                'message': message,
                'notification_type': 'chat_message'
            }
        )
    
    def chat_message(self, event):
        type = event["notification_type"]
        if type == "chat_message":
            message = event["message"]
            serializer = MessageSerializer(message)
            self.send(text_data=json.dumps({"type": "chat", "object": serializer.data}))
      