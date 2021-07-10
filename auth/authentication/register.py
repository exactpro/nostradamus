from passlib.context import CryptContext

from models.User import User
from models.UserSettings import UserSettings
from models.UserFilter import UserFilter
from models.UserQAMetricsFilter import UserQAMetricsFilter
from models.UserPredictionsTable import UserPredictionsTable

from serializers import UserSerializer

from settings.settings import init_filters, init_predictions_table


async def create_user(user: UserSerializer) -> None:
    """Creates a new User with default settings.

    :param user: New user.
    """
    user = user.dict()
    user["password"] = CryptContext(schemes=["sha256_crypt"]).hash(
        user["password"]
    )
    user["email"] = user["email"].lower().strip()
    user["name"] = user["name"].strip()
    user = await User(**user).create()
    user_settings = await UserSettings(user_id=user.id).create()

    await init_filters(UserFilter, user_settings.id)
    await init_filters(UserQAMetricsFilter, user_settings.id)
    await init_predictions_table(UserPredictionsTable, user_settings.id)
