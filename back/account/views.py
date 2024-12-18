from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from transaction.models import Reservation
from django.conf import settings
from django.utils.timezone import now, timedelta
from transaction.serializers import ReservationSerializer
from django.db.models import Count, Q
from post.serializers import PostSerializer
from post.models import Like
from django.db.models import Exists, OuterRef
from .pagination import CustomPageNumberPagination
from urllib.parse import urljoin
from .utils import generate_presigned_url
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def myposts(self, request, pk=None):
        user = request.user
        # Get page and page_size from query parameters
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
  
        liked_subquery = Like.objects.filter(
            post=OuterRef("pk"),  # Refers to the current post in the main queryset
            liked_by=user,
        )
        
        posts = user.posts.filter(is_active=True).annotate(liked=Exists(liked_subquery))
        
        
        paginated_queryset = self.paginate_queryset(posts)
        
        
        if paginated_queryset is not None:
            serializer = PostSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # If no pagination is applied, return all followers
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        follower = request.user
        followed = self.get_object()
        follower.following.add(followed)
        followed.followers.add(follower)
        return Response({'message': 'User followed successfully'})
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        unfollower = request.user
        followed = self.get_object()
        
        unfollower.following.remove(followed)
        followed.followers.remove(unfollower)
        
        return Response({'message': 'User unfollowed successfully'})
    @action(detail=False, methods=["PATCH"])
    def update_profile(self, request, pk=None):
        user = request.user
        avatar = request.FILES.get("avatar", None)

        if avatar:
            user.avatar = avatar 

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            password1 = request.data.get("password1", None)
            password2 = request.data.get("password2", None)

            if password1 and password2:
                if password1 != password2:
                    raise Response(
                        "Passwords do not match", status=status.HTTP_400_BAD_REQUEST
                    )
                user.set_password(password1)
                user.save()
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request, pk=None):
        user = request.user
        blocklist_threshold_date = now() - timedelta(days=settings.REPORTED_BLOCKLIST_DAYS)

        # Handle avatar URL based on FROM_S3 setting
        if user.avatar:
            if settings.FROM_S3 == "true":
                avatar_url = generate_presigned_url(user.avatar)
            else:
                # For local, use request.build_absolute_uri
                avatar_url = request.build_absolute_uri(user.avatar.url)
        else:
            avatar_url = None

        reported_reservation = Reservation.objects.filter(post__created_by=request.user, status='reported', reported_at__gte=blocklist_threshold_date).order_by('-reported_at').select_related('buyer', 'post', 'post__created_by').prefetch_related('post__images').first()
        is_reported_on = False
        if reported_reservation is not None:
            is_reported_on = True
            reported_reservation = ReservationSerializer(reported_reservation).data

        response_data = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "avatar": avatar_url,
            "coins": user.coins,
            "reported": is_reported_on,
            "reportedReservation": reported_reservation
        }

        return JsonResponse(response_data)
    @action(detail=False, methods=['get'])
    def stats(self, request, pk=None):
        user = request.user
        blocklist_threshold_date = now() - timedelta(days=settings.REPORTED_BLOCKLIST_DAYS)

        # Avatar URL
        if user.avatar:
            if settings.FROM_S3 == "true":
                avatar_url = generate_presigned_url(user.avatar)
            else:
                # For local, use request.build_absolute_uri
                avatar_url = request.build_absolute_uri(user.avatar.url)
        else:
            avatar_url = None

        # Pre-aggregate data
        stats = Reservation.objects.filter(
            Q(post__created_by=user) | Q(buyer=user)
        ).select_related('buyer', 'post', 'post__created_by').prefetch_related('post__images').aggregate(
            ordered_count=Count('id', filter=Q(post__created_by=user)),
            delivered_count=Count('id', filter=Q(post__created_by=user, status='completed')),
            reserved_count=Count('id', filter=Q(buyer=user)),
            received_count=Count('id', filter=Q(buyer=user, status='completed')),
            canceled_count=Count('id', filter=Q(buyer=user, status='cancelled')),
        )

        # Reported Reservation
        reported_reservation = Reservation.objects.filter(
            post__created_by=request.user,
            status='reported',
            reported_at__gte=blocklist_threshold_date
        ).order_by('-reported_at').select_related('buyer', 'post', 'post__created_by').prefetch_related('post__images').first()

        is_reported_on = False
        if reported_reservation is not None:
            is_reported_on = True
            reported_reservation = ReservationSerializer(reported_reservation).data

        # Response Data
        response_data = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "avatar": avatar_url,
            "coins": user.coins,
            "reported": is_reported_on,
            "reportedReservation": reported_reservation,
            "stats": {
                "ads": request.user.posts.filter(is_active=True).count(),
                "ordered": stats['ordered_count'],
                "delivered": stats['delivered_count'],
                "reserved": stats['reserved_count'],
                "received": stats['received_count'],
                "canceled": stats['canceled_count'],
                "coins_spent": user.coins_spent,
                "coins_bought": user.coins_bought,
            },
        }

        return JsonResponse(response_data)
