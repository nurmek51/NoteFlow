import urllib.parse
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication

@database_sync_to_async
def get_user_from_token(token):
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        return user
    except Exception as e:
        print("JWT token validation error:", e)
        return AnonymousUser()

class JWTAuthMiddleware:
    """
    Middleware for auth through JWT, which extracts the token from query string and puts the user in the scope.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = urllib.parse.parse_qs(query_string)
        token_list = query_params.get("token", None)
        token = token_list[0] if token_list else None

        if token:
            scope["user"] = await get_user_from_token(token)
            print(f"User authenticated: {scope['user']}")  # log of success auth
        else:
            scope["user"] = AnonymousUser()
            print("JWT Token is missing or invalid, setting AnonymousUser")

        print(f"Final user in scope: {scope['user']}")
        return await self.inner(scope, receive, send)

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)
