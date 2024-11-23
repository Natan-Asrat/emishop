from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, OrderViewSet

router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservations')

router.register('orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls))
]