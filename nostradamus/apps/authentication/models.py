from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.settings.main.common import init_filters, init_predictions_table


class User(AbstractUser):
    name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    REQUIRED_FIELDS = ["name", "email", "password"]

    class Meta:
        verbose_name = "User"

    @staticmethod
    def post_create(
        sender: models.Model,
        instance: models.Model,
        created: bool,
        *args,
        **kwargs,
    ) -> None:
        """Instance creating handler. Creates instance folders and
        default settings for it.

        Parameters:
        ----------
        sender:
            Object to which the handler should respond.
        instance:
            Instance of User model.
        created:
            True if new instance created, otherwise False.
        """

        def init_settings():
            """Init all default user's settings"""
            init_filters(UserFilter, user_settings)
            init_filters(UserQAMetricsFilter, user_settings)
            init_predictions_table(UserPredictionsTable, user_settings)

        if created:
            from apps.settings.models import (
                UserSettings,
                UserFilter,
                UserQAMetricsFilter,
                UserPredictionsTable,
            )

            user_settings = UserSettings.objects.create(user=instance)
            init_settings()

    def __str__(self):
        return self.email


class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Team"

    @staticmethod
    def post_create(
        sender: models.Model,
        instance: models.Model,
        created: bool,
        *args,
        **kwargs,
    ) -> None:
        """Instance creating handler. Creates instance folders and
        default settings for it.

        Parameters:
        ----------
        sender:
            Object to which the handler should respond.
        instance:
            Instance of Team model.
        created:
            True if new instance created, otherwise False.
        """
        if created:
            from apps.settings.models import (
                TeamSettings,
                TeamFilter,
                TeamQAMetricsFilter,
                TeamPredictionsTable,
            )

            team_settings = TeamSettings.objects.create(team=instance)

            init_filters(TeamFilter, team_settings)
            init_filters(TeamQAMetricsFilter, team_settings)
            init_predictions_table(TeamPredictionsTable, team_settings)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Role"

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.team} {self.role}"


post_save.connect(Team.post_create, sender=Team)
post_save.connect(User.post_create, sender=User)
