from rest_framework import serializers
from .models import Conversation, Message
from account.serializers import UserSerializer
from post.serializers import PostSerializer
from transaction.serializers import ReservationSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "message", "title", "sender", "reservation", "type", "user", "post", "read", "created_at_formatted"]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'buyer', 'seller', 'created_at', 'updated_at', 'created_at_formatted', 'updated_at_formatted']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'sent_at', 
                 'seen_by_recipient', 'seen_by_sender', 'reservation', 'sent_at_formatted']
        read_only_fields = ['id', 'sent_at', 'seen_by_recipient', 'seen_by_sender']

class MessageListSerializer(serializers.Serializer):
    type = serializers.CharField(default="chat")
    object = MessageSerializer(many=True)  # This will handle a list of Message objects
    
    def to_representation(self, instance):
        # Here we're overriding to ensure the correct format
        data = super().to_representation(instance)
        if isinstance(instance, list):
            return [{"type": "chat", "object": message} for message in instance]
        else:
            return {"type": "chat", "object": data['object']}