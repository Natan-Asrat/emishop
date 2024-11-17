from rest_framework import serializers
from .models import Conversation, Message
from account.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'buyer', 'seller', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'sent_at', 
                 'seen_by_recipient', 'seen_by_sender', 'reservation']
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