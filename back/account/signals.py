from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import User

@receiver(m2m_changed, sender=User.following.through)
def update_following_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.following_count = instance.following.count()
        instance.save()

@receiver(m2m_changed, sender=User.followers.through)
def update_follower_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        instance.follower_count = instance.followers.count()
        instance.save()
