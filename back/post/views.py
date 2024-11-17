from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from pgvector.django import CosineDistance
import json
from rest_framework import status

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['POST', 'GET'])
    def feed(self, request):
        user_embedding = request.data.get('user_embedding')
        
        if user_embedding:
            # Convert string to list of floats
            if isinstance(user_embedding, str):
                user_embedding = [float(x) for x in user_embedding.split(',')]
            elif isinstance(user_embedding, list):
                user_embedding = [float(x) for x in user_embedding]      
            posts = Post.objects.annotate(
                similarity=CosineDistance('embedding', user_embedding)
            ).order_by('similarity')[:1]

        else:
            # If no user embedding, return diverse range of posts
            posts = Post.objects.order_by('?')[:20]
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

