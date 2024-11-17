from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, PostImage

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()  # Change image_url to images

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'images', 'price', 'currency', 'quantity', 'tags', 'embedding', 'created_at', 'updated_at']

    def get_images(self, obj):
        # Get all related images for the post
        image_urls = [self.context['request'].build_absolute_uri(image.image.url) for image in obj.images.all()]
        return image_urls  # Return list of image URLs


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    )

    class Meta:
        model = Post
        fields = ['title', 'images', 'price', 'currency', 'quantity', 'tags', 'embedding']

    def create(self, validated_data):
        images = validated_data.pop('images')
        post = Post.objects.create(**validated_data)

        for image in images:
            PostImage.objects.create(post=post, image=image)

        return post