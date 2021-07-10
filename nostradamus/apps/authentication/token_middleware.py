import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None

        request_verifying = requests.get(
            "http://auth:8080/verify_token/", params={"token": token}
        )

        response = request_verifying.json()

        if request_verifying.status_code != 200:
            raise AuthenticationFailed(response.get("exception").get("detail"))

        user = User.objects.get(id=response.get("id"))

        return (user, None)
