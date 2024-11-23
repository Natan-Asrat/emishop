from django.shortcuts import render
from .models import Conversation, Message
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer, NotificationSerializer
from .models import Notification
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    @action(detail=True, methods=['GET'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
