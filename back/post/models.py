from django.db import models
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from pgvector.django import VectorField
import math
import uuid
from django.utils.timesince import timesince
# Create your models here.
class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    quantity = models.PositiveIntegerField()
    initial_quantity = models.PositiveIntegerField()
    tags = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    embedding = VectorField(
        dimensions=512,
        help_text="Vector embeddings (clip-vit-large-patch14) of the file content",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    def get_required_coins(self):
        return math.ceil(float(self.price) * 0.01)

    def __str__(self):
        return self.title
class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f'Image for {self.post.title}'


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ForeignKey(
        "account.User", related_name="likes", on_delete=models.CASCADE, null=True
    )
    post = models.ForeignKey(
        "post.Post", related_name="likes", on_delete=models.CASCADE, null=True
    )

