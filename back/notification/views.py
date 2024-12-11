
from django.shortcuts import render
from .models import Conversation, Message
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ConversationSerializer, MessageSerializer, NotificationSerializer
from .models import Notification
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.select_related('buyer', 'seller').all()
    serializer_class = ConversationSerializer
    pagination_class = CustomPageNumberPagination
    @action(detail=True, methods=['GET'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation).select_related('sender').order_by('-sent_at')
        
        paginated_messages = self.paginate_queryset(messages)
        
        if paginated_messages is not None:
            serializer = MessageSerializer(paginated_messages, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class NotificationViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).select_related('post', 'user', 'sender', 'reservation', 'post__created_by', 'reservation__buyer', 'reservation__post', 'reservation__post__created_by').prefetch_related('post__images', 'reservation__post__images')
        notification_type = self.request.query_params.get('type')

        if notification_type == 'reservations':
            queryset = queryset.filter(
                Q(type='reservation') | 
                Q(type='status_update') | 
                Q(type='popup', reservation__isnull=False)
            )
        elif notification_type == 'posts':
            queryset = queryset.filter(
                Q(type='like') | 
                Q(type='popup', post__isnull=False)
            )
        elif notification_type == 'messages':
            queryset = queryset.filter(type='message')
        elif notification_type == 'all':  # Include all unread notifications
            queryset = queryset.filter(read=False)

        return queryset
    @action(detail=False, methods=['GET'])
    def count(self, request, pk=None):
        user = request.user

        # Base queryset for unread notifications
        unread_notifications = Notification.objects.filter(user=user, read=False)

        # Count for reservations
        reservation_count = unread_notifications.filter(
            Q(type='reservation') | 
            Q(type='status_update') | 
            Q(type='popup', reservation__isnull=False)
        ).count()

        # Count for posts
        post_count = unread_notifications.filter(
            Q(type='like') | 
            Q(type='popup', post__isnull=False)
        ).count()

        # Count for messages
        message_count = unread_notifications.filter(type='message').count()

        # Total count for all unread notifications
        total_count = unread_notifications.count()

        # Build the response
        data = {
            'reservations': reservation_count,
            'posts': post_count,
            'messages': message_count,
            'all': total_count,
        }

        return Response(data)
