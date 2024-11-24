from django.db import models
from django.utils.timesince import timesince
from datetime import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class Notification(models.Model):
    TYPE_CHOICES = [
        ('reservation', 'New Reservation'),
        ('message', 'New Message'),
        ('like', 'New Like'),
        ('status_update', 'Status Update'),
        ('popup', 'Show Popup')
    ]

    user = models.ForeignKey('account.User', related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey('account.User', related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey('transaction.Reservation', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['-created_at']
    @property
    def created_at_formatted(self):
        return timesince(self.created_at)


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey('account.User', related_name='conversations_as_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey('account.User', related_name='conversations_as_seller', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def created_at_formatted(self):
        return timesince(self.created_at)
    @property
    def updated_at_formatted(self):
        return timesince(self.updated_at)
class Message(models.Model):
    sender = models.ForeignKey('account.User', related_name='sent_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    seen_by_recipient = models.BooleanField(default=False)
    seen_by_sender = models.BooleanField(default=False)
    reservation = models.ForeignKey('transaction.Reservation', related_name='messages', 
                                  on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def sent_at_formatted(self):
        return timesince(self.created_at)

    def delete_if_old(self):
        if timezone.now() - self.sent_at > timezone.timedelta(days=30):
            self.delete()


@receiver(post_save, sender=Notification)
def send_notification_to_group(sender, instance, created, **kwargs):
    if created:
        # Fetch the user who the notification is for
        user = instance.user

        # Send the notification to the user's notification group
        group_name = f"notify_{user.id}"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "notification_handler",
                "notification_type": "notification",
                "notification": instance,
            },
        )
