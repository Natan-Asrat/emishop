"""
ASGI config for back project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")
django.setup()

# Import after django setup
from notification.ws_middleware import JWTAuthMiddleware
from notification import routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": 
            JWTAuthMiddleware(URLRouter(routing.ws_urlpatterns))
        
    }
)
