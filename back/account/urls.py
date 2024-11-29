from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet
from .payment_views import create_paypal_order, capture_paypal_order

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create-paypal-order/", create_paypal_order, name="create-paypal-order"),
    path("capture-paypal-order/", capture_paypal_order, name="capture-paypal-order"),
]
