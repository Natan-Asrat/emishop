from django.shortcuts import render
from .models import Reservation
from .serializers import ReservationSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from post.models import Post
from notification.models import Notification, Conversation
from django_filters.rest_framework import DjangoFilterBackend
from notification.serializers import ConversationSerializer
import logging
from django.utils import timezone
from django.db.models import Count
logger = logging.getLogger(__name__)

# Create your views here.
class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    def get_queryset(self):
        if self.action == 'list':
            return Reservation.objects.filter(buyer=self.request.user).order_by('-created_at')
        return Reservation.objects.all()
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        quantity = int(request.data.get('quantity', 1))
        post = get_object_or_404(Post, id=post_id)
        required_coins = post.get_required_coins() * quantity
        buyer = request.user
        # post_obj = Post.objects.select_for_update().get(id=post_id)
        if buyer.coins < required_coins:
            return Response(
                {'error': 'Insufficient coins'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if post.quantity < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create reservation and update coins/quantity
        print('Creating reservation')
        reservation = Reservation.objects.create(
            buyer=request.user,
            post=post,
            quantity=quantity,
            coins_spent=required_coins
        )
        buyer.coins -= required_coins
        buyer.save()
        post.quantity = post.quantity - quantity
        post.save()
        print("createing notification")
        # Create notification for seller
        message = f'{request.user.username} has reserved {quantity} quantity of item {post.title}'
        Notification.objects.create(
            user=post.created_by,
            type='reservation',
            title='You have a new reservation!',
            message=message,
            reservation=reservation
        )

        response_data = {
            'id': reservation.id,
            'buyer': reservation.buyer.username,
            'post_id': reservation.post.id,
            'quantity': reservation.quantity,
            'coins_spent': reservation.coins_spent,
            'created_at': reservation.created_at.isoformat()  # or any other fields you want to include
        }
        print('response', response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def count(self, request, pk=None):
        # Initialize result with all statuses set to 0
        statuses = dict.fromkeys([status[0] for status in Reservation.STATUS_CHOICES], 0)

        # Query counts grouped by status
        status_counts = (
            Reservation.objects.filter(buyer=request.user)
            .values('status')  # Group by status
            .annotate(count=Count('status'))  # Count occurrences of each status
        )

        # Update the initial dictionary with actual counts
        for item in status_counts:
            statuses[item['status']] = item['count']

        return Response(statuses)
    @action(detail=True, methods=['POST'])
    def complete(self, request, pk=None):
        reservation = self.get_object()
        if reservation.buyer != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reservation.status = 'completed'
        reservation.save()
        
        # Notify seller
        Notification.objects.create(
            user=reservation.post.created_by,
            type='status_update',
            title='Reservation Completed!',
            message=f'Received item {reservation.post.title} by buyer {reservation.buyer.username}!',
            reservation=reservation
        )
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.buyer != request.user and reservation.post.created_by != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        with transaction.atomic():
            # Refund coins if cancelled by seller
            if request.user == reservation.post.created_by:
                buyer = reservation.buyer
                buyer.coins += reservation.coins_spent
                buyer.save()
            
            # Return quantity to post
            post = Post.objects.select_for_update().get(id=reservation.post.id)
            post.quantity = F('quantity') + reservation.quantity
            post.save()
            
            reservation.status = 'cancelled'
            reservation.cancelled_by = request.user
            reservation.save()
        
        # Notify other party
        notify_user = reservation.buyer if request.user == reservation.post.created_by else reservation.post.created_by
        Notification.objects.create(
            user=notify_user,
            type='status_update',
            title='Reservation Canceled!',
            message=f'Canceled reservation for item {reservation.post.title} by buyer {reservation.buyer.username}!',
            reservation=reservation
        )
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def report(self, request, pk=None):
        reason = request.data.get('reason')
        reservation = self.get_object()
        if reservation.buyer != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reservation.status = 'reported'
        reservation.report_reason = reason
        reservation.reported_at = timezone.now()
        reservation.save()
        
        # Notify seller
        Notification.objects.create(
            user=reservation.post.created_by,
            type='popup',
            title=f"Reservation reported! Have you delivered the item? Reason: '{reason}'",
            message=f"Reported reservation for item '{reservation.post.title}' by buyer '{reservation.buyer.username}' for reason '{reason}'!",
            reservation=reservation
        )
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def conversation(self, request, pk=None):
        reservation = self.get_object()
        buyer = reservation.buyer
        seller = reservation.post.created_by
        conversation = Conversation.objects.filter(buyer=buyer, seller=seller)
        if conversation.exists():
            conversation = conversation.first()
        else:
            conversation = Conversation.objects.create(
                buyer=buyer,
                seller=seller
            )
        conversation_serializer = ConversationSerializer(conversation)
        reservation_serializer = self.get_serializer(reservation)
        data = {
            'conversation': conversation_serializer.data,
            'reservation': reservation_serializer.data
        }
        return Response(data)
 
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    def get_queryset(self):
        if self.action == 'list':
            return Reservation.objects.filter(post__created_by=self.request.user).order_by('-created_at')
        return Reservation.objects.all()

    @action(detail=False, methods=['GET'])
    def count(self, request, pk=None):
        # Initialize result with all statuses set to 0
        statuses = dict.fromkeys([status[0] for status in Reservation.STATUS_CHOICES], 0)

        # Query counts grouped by status
        status_counts = (
            Reservation.objects.filter(post__created_by=request.user)
            .values('status')  # Group by status
            .annotate(count=Count('status'))  # Count occurrences of each status
        )

        # Update the initial dictionary with actual counts
        for item in status_counts:
            statuses[item['status']] = item['count']

        return Response(statuses)
    @action(detail=True, methods=['POST'])
    def accept(self, request, pk=None):
        reservation = self.get_object()
        if reservation.post.created_by != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reservation.seller_accepted = True
        reservation.save()
        
        # Notify buyer
        Notification.objects.create(
            user=reservation.buyer,
            type='status_update',
            title='Reservation Accepted',
            message=f'Your reservation for {reservation.post.title} has been accepted! You should message the sender now in Transactions tab!',
            reservation=reservation
        )

        serializer = self.get_serializer(reservation)
        return Response(serializer.data)
        

    @action(detail=True, methods=['POST'])
    def complete(self, request, pk=None):
        reservation = self.get_object()
        if reservation.post.created_by != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Notify buyer
        Notification.objects.create(
            user=reservation.buyer,
            type='popup',
            title='Have you received the item?',
            message=f'Seller claims you have received item {reservation.post.title}, please confirm if you have received it by going to transactions page, or ignore this otherwise!',
            reservation=reservation
        )
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.buyer != request.user and reservation.post.created_by != request.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        with transaction.atomic():
            # Refund coins if cancelled by seller
            if request.user == reservation.post.created_by:
                buyer = reservation.buyer
                buyer.coins += reservation.coins_spent
                buyer.save()
            
            # Return quantity to post
            post = Post.objects.select_for_update().get(id=reservation.post.id)
            post.quantity = F('quantity') + reservation.quantity
            post.save()
            
            reservation.status = 'cancelled'
            reservation.cancelled_by = request.user
            reservation.save()
        
        # Notify other party
        notify_user = reservation.buyer if request.user == reservation.post.created_by else reservation.post.created_by
        Notification.objects.create(
            user=notify_user,
            type='status_update',
            title='Reservation Canceled!',
            message=f'Canceled reservation for item {reservation.post.title} by seller {reservation.post.created_by.username}!',
            reservation=reservation
        )
        
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def conversation(self, request, pk=None):
        reservation = self.get_object()
        buyer = reservation.buyer
        seller = reservation.post.created_by
        conversation = Conversation.objects.filter(buyer=buyer, seller=seller)
        if conversation.exists():
            conversation = conversation.first()
        else:
            conversation = Conversation.objects.create(
                buyer=buyer,
                seller=seller
            )
        conversation_serializer = ConversationSerializer(conversation)
        reservation_serializer = self.get_serializer(reservation)
        data = {
            'conversation': conversation_serializer.data,
            'reservation': reservation_serializer.data
        }
        return Response(data)
 