from apps.authentication.models import Role, TeamMember
from utils.const import DEFAULT_ROLE


def bind_user_to_team(user_instance, team):
    """ Binds user with team.

    Parameters:
    ----------
    user_instance:
        User instance.
    team:
        Team to which user will be attached.
    """
    team_member_instance = TeamMember(
        user=user_instance, team=team, role=get_default_role(),
    )
    team_member_instance.save()


def get_default_role():
    """ Returns default role.
    """
    return Role.objects.get(name=DEFAULT_ROLE)
