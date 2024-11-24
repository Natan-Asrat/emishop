from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Like
from django.db.models import OuterRef, Exists
from .serializers import PostSerializer, PostCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from pgvector.django import CosineDistance
import json
from rest_framework import status
from notification.models import Notification
from rest_framework.filters import SearchFilter
from django.utils.timezone import now, timedelta
from django.conf import settings
from transaction.models import Reservation
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    filter_backends = (SearchFilter,)
    search_fields = [
        'title',
        'tags',
        'created_by__username',
        'created_by__name', 
    ]
    def get_queryset(self):
        queryset = self.queryset
        if(self.action == 'create'):
            return queryset
        liked_subquery = Like.objects.filter(
            post=OuterRef("pk"),  # Refers to the current post in the main queryset
            liked_by=self.request.user,
        )
        queryset = queryset.annotate(liked=Exists(liked_subquery))
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(liked_by=user, post=post)
        if created:
            post.likes_count = post.likes.count()
            post.save()
        post.liked = True
        serializer = self.get_serializer(post)
        notification_message = f"{user.username} liked your post {post.title}!"
        Notification.objects.create(
            user=post.created_by,
            type='like',
            title="Your post has got a new like!",
            message=notification_message,
            post=post
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(liked_by=user, post=post)
            like.delete()
            post.liked = False

            post.likes_count = post.likes.count()
            post.save()
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['GET'])
    def favourites(self, request):
        liked_posts = Post.objects.filter(likes__liked_by=request.user)
        serializer = self.get_serializer(liked_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST', 'GET'])
    def feed(self, request):
        blocklist_threshold_date = now() - timedelta(days=settings.REPORTED_BLOCKLIST_DAYS)

        # Subquery for sellers with reported reservations
        reported_seller_ids = Reservation.objects.filter(
            status='reported',
            reported_at__gte=blocklist_threshold_date
        ).values_list('post__created_by_id', flat=True)

        user_embedding = request.data.get('user_embedding')
        
        liked_subquery = Like.objects.filter(
            post=OuterRef("pk"),  # Refers to the current post in the main queryset
            liked_by=request.user,
        )
        if user_embedding:
            # Convert string to list of floats
            if isinstance(user_embedding, str):
                user_embedding = [float(x) for x in user_embedding.split(',')]
            elif isinstance(user_embedding, list):
                user_embedding = [float(x) for x in user_embedding]      
            posts = Post.objects.annotate(
                    similarity=CosineDistance('embedding', user_embedding),
                    liked=Exists(liked_subquery)
                ).exclude(created_by__id__in=reported_seller_ids).order_by('similarity')[:1]

        else:
            # Exclude posts from reported sellers and return diverse range of posts
            posts = Post.objects.exclude(
                created_by__id__in=reported_seller_ids
            ).order_by('?').annotate(liked=Exists(liked_subquery))[:20]

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    @action(detail=False, methods=['POST'], url_path='create-new')
    def create_new(self, request, *args, **kwargs):
        """
        Custom action to handle `create_new_post` logic directly within the ViewSet.
        """
        # Extract data from request
        title = request.data.get("title")
        price = request.data.get("price")
        currency = request.data.get("currency")
        quantity = request.data.get("quantity")
        tags = request.data.get("tags", [])
        images = request.FILES.getlist("images")
        embedding = []
        for i in range(512):
            value = request.data.get(f'embedding[{i}]')
            if value is not None:
                embedding.append(float(value)) 
        # Convert tags and embedding if provided as JSON strings
        if isinstance(tags, str):
            tags = json.loads(tags)
        
        # Validate and create the post using PostCreateSerializer
        
        serializer = self.get_serializer(data={
            "title": title,
            "price": price,
            "currency": currency,
            "quantity": quantity,
            "tags": tags,
            "initial_quantity": quantity,
            "embedding": embedding,
            # "images": images,
        })
        serializer.is_valid(raise_exception=True)

        # Save the post
        post = serializer.save(created_by=request.user)
        for image in images:
            post.images.create(image=image) 
        # Return the created post data
        response_serializer = PostSerializer(post, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

