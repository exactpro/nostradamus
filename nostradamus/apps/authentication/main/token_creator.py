from rest_framework_simplejwt.tokens import AccessToken

from apps.authentication.models import User, Team, Role, TeamMember
from utils.exceptions import IncorrectUserCredentials


class TokenCreator:
    def __init__(self, credentials, password):
        self.password = password
        self.credentials = credentials
        self.__user = self.__get_user()

    def create_jwt(self) -> dict:
        """" Generates jwt with user data if input credentials are valid.

        Returns:
        ----------
            Jwt with 15 weeks expiration date.
        """

        if self.__check_password():
            payload = self.__create_jwt_payload()
            payload["token"] = str(AccessToken.for_user(self.__user))

            return payload

    def __create_jwt_payload(self) -> dict:
        """" Receives all information about __user object.

        Returns:
        ----------
            User information.
        """

        payload = {
            "id": self.__user.id,
            "name": self.__user.name,
            "email": self.__user.email,
        }

        team_member = TeamMember.objects.filter(user=self.__user).first()
        team = Team.objects.filter(id=team_member.team.id).first().name
        role = Role.objects.filter(id=team_member.role.id).first().name

        payload["team"] = team
        payload["role"] = role

        return payload

    def __check_password(self) -> bool:
        """" Checks that user and user password are valid.

        Returns:
        ----------
            True if user sent valid credentials otherwise False.
        """

        if self.__user and self.__user.check_password(self.password):
            return True

        raise IncorrectUserCredentials

    def __get_user(self) -> User:
        """" Generates private User object for password checking.

        Returns:
        ----------
            User object which can be accessed only inside TokenCreator class.
        """

        query = User.objects.filter(name__iexact=self.credentials)

        if query:
            return query.first()

        query = User.objects.filter(email__iexact=self.credentials)

        if query:
            return query.first()
