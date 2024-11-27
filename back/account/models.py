from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

class CustomUserManager(BaseUserManager):
    def normalize_username(self, username):
        # Normalize the username by converting it to lowercase
        return username.lower()
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    following = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    USERNAME_FIELD='username'
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    coins = models.IntegerField(default=0)
    coins_spent = models.IntegerField(default=0)
    coins_bought = models.IntegerField(default=0)

    objects = CustomUserManager()

    def natural_key(self):
        return (self.username,)

    def __str__(self):
        return self.username
    
@receiver(pre_save, sender=User)
def update_coin_stats(sender, instance, **kwargs):
    # Check if this is an update and not a new user creation
    if not instance._state.adding:
        # Get the old user instance from the database
        old_instance = User.objects.get(pk=instance.pk)
        
        # Calculate the difference in coins
        coin_difference = instance.coins - old_instance.coins
        
        # Adjust coins_bought or coins_spent based on the difference
        if coin_difference > 0:
            instance.coins_bought += coin_difference
        elif coin_difference < 0:
            instance.coins_spent += abs(coin_difference)