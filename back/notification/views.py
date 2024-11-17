from django.shortcuts import render
from .models import Conversation, Message
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer
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
    