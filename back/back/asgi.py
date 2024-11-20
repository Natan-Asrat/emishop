"""
ASGI config for back project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from notification.ws_middleware import JWTAuthMiddleware
from django.core.asgi import get_asgi_application
from notification import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")

def get_application():
    from notification.routing import ws_urlpatterns
    return ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": AllowedHostsOriginValidator(
                JWTAuthMiddleware(URLRouter(routing.ws_urlpatterns))
            ),
        }
    )

application = get_application()
