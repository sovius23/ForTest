from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

Profile = get_user_model()


@database_sync_to_async
def get_user(token):
    try:
        return Token.objects.get(key=token).user
    except Exception:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        try:
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            scope['user'] = await get_user(token)
        except Exception:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
