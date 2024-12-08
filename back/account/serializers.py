from rest_framework import serializers
from .models import User
from django.conf import settings
from urllib.parse import urljoin


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", 
            "name", 
            "username", 
            "follower_count", 
            "following_count", 
            "posts_count", 
            "avatar"
            ]

    def get_avatar(self, obj):
        if obj.avatar:
            base_url = settings.SITE_URL  
            media_url = settings.MEDIA_URL
            if settings.FROM_S3 == "true":
                avatar_url = urljoin(
                    media_url + str(obj.avatar)
                )  
            else:
                avatar_url = urljoin(
                    base_url, media_url + str(obj.avatar)
                )  
            return avatar_url
        return None

# class UserCreateSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'name', 'password1', 'password2', 'avatar']
    
#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError("Passwords must match.")
#         return data

#     def create(self, validated_data):
#         password = validated_data.pop('password1')
#         user = User(**validated_data)
#         user.set_password(password)  # Hash the password
#         user.save()
#         return user
    
class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'password1', 'password2', 'avatar']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data
        validated_data.pop('password2', None)

        # Extract password1 and create user object
        password = validated_data.pop('password1')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
