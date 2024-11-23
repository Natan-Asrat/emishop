from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, NotificationViewSet

router = DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversations') 
router.register('notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]
