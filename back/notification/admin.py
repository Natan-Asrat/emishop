from django.contrib import admin
from .models import Notification, Message, Conversation

# Register your models here.
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Conversation)