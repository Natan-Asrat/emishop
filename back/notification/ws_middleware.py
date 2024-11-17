import jwt
from datetime import datetime
from channels.auth import AuthMiddlewareStack
from channels.exceptions import DenyConnection
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from urllib.parse import parse_qs


class JWTAuthMiddleware:
    """
    Custom middleware for JWT authentication for Django Channels WebSockets.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract the token from query params or headers
        token = None
        query_string = parse_qs(scope.get("query_string", b"").decode())
        if "token" in query_string:
            token = query_string["token"][0]  # e.g., ?token=<jwt_token>

        if token:
            try:
                # Decode the token using the same secret as in your settings.py
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

                # If the token is valid, the user should be authenticated
                scope["user"] = (
                    payload  # You can also attach the user to the scope if needed
                )

            except jwt.ExpiredSignatureError:
                raise DenyConnection("Token has expired.")
            except jwt.DecodeError:
                raise DenyConnection("Invalid token.")

        # Call the inner application (this will continue to the WebSocket consumer)
        return await self.inner(scope, receive, send)
