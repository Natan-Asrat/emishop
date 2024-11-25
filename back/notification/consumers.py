from channels.generic.websocket import WebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from asgiref.sync import async_to_sync
import json
from notification.models import Notification, Conversation
from notification.serializers import NotificationSerializer
import time
from post.serializers import PostSerializer
from post.models import connected_users

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.conversation = Conversation.objects.get(id=self.conversation_id)
        self.user_id = self.user.get("user_id", None)
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_id, self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.conversation_id, self.channel_name)
        super().disconnect(close_code)
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        reservation_id = data.get('reservation_id')
        buyer = self.conversation.buyer
        seller = self.conversation.seller
        if str(self.user_id) == str(buyer.id):
            sender = buyer
            receiver = seller
        elif str(self.user_id) == str(seller.id):
            sender = seller
            receiver = buyer
        else:
            return
        if reservation_id:
            message = Message.objects.create(
                sender_id = self.user_id,
                conversation_id = self.conversation_id,
                content = data.get('message'),
                reservation_id = reservation_id
            )
            
            Notification.objects.create(
                user = receiver,
                sender = sender,
                type='message',
                title=f"You have a new message from '{sender.username}!'",
                message=data.get('message'),
                reservation_id = reservation_id
            )
        else:
            message = Message.objects.create(
                sender_id = self.user_id,
                conversation_id = self.conversation_id,
                content = data.get('message')
            )
            
            Notification.objects.create(
                user = receiver,
                sender = sender,
                type='message',
                title=f"You have a new message from '{sender.username}!'",
                message=data.get('message'),
            )
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_id,
            {
                'type': 'chat_message',
                'message': message,
                'notification_type': 'chat_message'
            }
        )
    
    def chat_message(self, event):
        type = event["notification_type"]
        if type == "chat_message":
            message = event["message"]
            serializer = MessageSerializer(message)
            self.send(text_data=json.dumps({"type": "chat", "object": serializer.data}))

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.user_id = self.user.get("user_id", None)

        self.post_groups = set()
        self.group_name = f"notify_{self.user_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()   
        self.send_notifications_with_delay()
    def get_last_delivered_notification(self):
        return (
            Notification.objects.filter(
                user_id = self.user_id,
                read = True
            ).order_by("-created_at")
            .first()
        )
    def get_undelivered_notifications(self, last_delivered_at=None):
        if last_delivered_at:
            return (
                Notification.objects.filter(
                    user_id = self.user_id,
                    read = False,
                    created_at__gt = last_delivered_at
                ).order_by("-created_at")
            )
        else:
            return (
                Notification.objects.filter(
                    user_id = self.user_id,
                    read = False
                ).order_by("-created_at")
            )
    def send_notifications_with_delay(self):
        last_delivered_notification = self.get_last_delivered_notification()
        if last_delivered_notification:
            undelivered_notifications = self.get_undelivered_notifications(last_delivered_notification.created_at)
        else:
            undelivered_notifications = self.get_undelivered_notifications()
        for notification in undelivered_notifications:
            notification_data = NotificationSerializer(notification).data
            message = {"type": "notification", "object": notification_data}
            self.send(text_data=json.dumps(message))
            time.sleep(3)
    def disconnect(self, code):
        self.unsubscribe_from_post_groups()
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        return super().disconnect(code)
    def notification_handler(self, event):
        type = event["notification_type"]
        if type == "post":
            post = event["post"]
            post_data = PostSerializer(post).data
            message = {"type": "post", "object": post_data}
            self.send(text_data=json.dumps(message))
        elif type == "notification":
            notification = event["notification"]
            notification_data = NotificationSerializer(notification).data
            message = {"type": "notification", "object": notification_data}
            self.send(text_data = json.dumps(message))
    def subscribe_to_post_group(self, post_id):
        """Adds the user to the post group if not already added."""

        post_group_name = f"post_{post_id}"
        if post_group_name not in connected_users:
            connected_users[post_group_name] = set()
        if self.user_id not in connected_users[post_group_name]:
            connected_users[post_group_name].add(self.user_id)
            self.post_groups.add(post_id)
    def unsubscribe_from_post_group(self, post_id):
        """Removes the user from the post group and removes the group if empty."""

        post_group_name = f"post_{post_id}"
        if post_group_name in connected_users:
            connected_users[post_group_name].discard(self.user_id)
            if len(connected_users[post_group_name]) == 0:
                del connected_users[post_group_name]
            self.post_groups.discard(post_id)
    def subscribe_to_post_groups(self, post_ids):
        """Subscribe to multiple post groups based on post_ids."""

        for post_id in post_ids:
            self.subscribe_to_post_group(post_id)

    def unsubscribe_from_post_groups(self):
        """Unsubscribe from all post groups the user is subscribed to."""

        for post_id in list(self.post_groups):
            self.unsubscribe_from_post_group(post_id)
    def subscribe_to_post_group_handler(self, event):
        post_id = event["post_id"]
        self.subscribe_to_post_group(post_id)
