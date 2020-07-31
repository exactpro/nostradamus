from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from apps.authentication.main.common import bind_user_to_team

from apps.authentication.serializers import (
    TeamSerializer,
    UserSerializer,
    AuthRequestSerializer,
    AuthResponseSerializer,
)
from apps.authentication.main.token_creator import TokenCreator
from apps.authentication.models import Team


class AuthenticationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        query_serializer=AuthRequestSerializer,
        responses={200: AuthResponseSerializer},
    )
    def post(self, request):
        credentials_serializer = AuthRequestSerializer(data=request.GET)
        credentials_serializer.is_valid(raise_exception=True)
        credentials, password = credentials_serializer.get_credentials()

        token_payload = TokenCreator(credentials, password).create_jwt()

        return Response(token_payload)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: TeamSerializer})
    def get(self, request):
        teams = Team.objects.all()

        teams_serializer = TeamSerializer(teams, many=True)
        data = teams_serializer.data
        return Response(data)

    @swagger_auto_schema(
        query_serializer=UserSerializer, responses={200: "success"}
    )
    def post(self, request):
        user_serializer = UserSerializer(data=request.GET)

        user_serializer.is_valid(raise_exception=True)
        team = user_serializer.get_team()
        user = user_serializer.save()

        bind_user_to_team(user, team)

        return Response({"result": "success"})
