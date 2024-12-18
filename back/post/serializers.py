from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, PostImage
from django.conf import settings
from urllib.parse import urljoin
from .utils import generate_presigned_url
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()  # Change image_url to images
    liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'is_active', 'liked', 'created_by', 'title', 'images', 'price', 'currency', 'quantity', 'initial_quantity', 'tags', 'embedding', 'created_at', 'updated_at', 'created_at_formatted', 'updated_at_formatted']

    def get_images(self, obj):
        image_urls = []
        for image in obj.images.all():
            if image.image:
                base_url = settings.SITE_URL
                media_url = settings.MEDIA_URL
                if settings.FROM_S3 == "true":
                    image_url = generate_presigned_url(image.image)
                else:
                    image_url = urljoin(
                        base_url, 
                        media_url + str(image.image)
                    )
                image_urls.append(image_url)
        return image_urls


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    )

    class Meta:
        model = Post
        fields = ['title', 'images', 'price', 'currency', 'initial_quantity', 'quantity', 'tags', 'embedding']

    def create(self, validated_data):
        images = validated_data.pop('images')
        post = Post.objects.create(**validated_data)

        for image in images:
            PostImage.objects.create(post=post, image=image)

        return post