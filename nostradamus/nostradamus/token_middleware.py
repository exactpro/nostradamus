import requests
from channels.auth import AuthMiddlewareStack

import os

from utils.exceptions import IncorrectUserCredentials

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        token = f"{self.get_token(scope)}"
        token_body = {"token": token}

        backend_host = "http://auth:8080"
        token_verify_route = "/token_verify/"

        request = requests.get(
            backend_host + token_verify_route, params=token_body
        )
        if request.status_code == 401:
            raise IncorrectUserCredentials

        return self.inner(scope)

    def get_token(self, scope):
        return scope["query_string"].decode("utf-8").split("=")[1]


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(
    AuthMiddlewareStack(inner)
)
