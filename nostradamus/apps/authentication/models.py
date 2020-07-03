import shutil

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.analysis_and_training.main.common import (
    init_instance_folders,
    get_team_dir,
    get_user_dir,
)
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
        """ Instance creating handler. Creates instance folders and
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
            """ Init all default user's settings
            """
            init_filters(UserFilter, user_settings)
            init_filters(UserQAMetricsFilter, user_settings)
            init_predictions_table(UserPredictionsTable, user_settings)
            init_archive(instance)

        if created:
            from apps.settings.models import (
                UserSettings,
                UserFilter,
                UserQAMetricsFilter,
                UserPredictionsTable,
            )
            from apps.settings.main.archiver import init_archive

            instance_dir = get_user_dir(instance)
            init_instance_folders(instance_dir)

            user_settings = UserSettings.objects.create(user=instance)
            init_settings()

    @staticmethod
    def post_delete(
        sender: models.Model, instance: models.Model, *args, **kwargs
    ) -> None:
        """ Instance deleting handler. Deletes instance folders.

        Parameters:
        ----------
        sender:
            Object to which the handler should respond.
        instance:
            Instance of User model.
        """
        instance_dir = get_user_dir(instance)
        shutil.rmtree(instance_dir)

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
        """ Instance creating handler. Creates instance folders and
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

            instance_dir = get_team_dir(instance)
            init_instance_folders(instance_dir)

            team_settings = TeamSettings.objects.create(team=instance)

            init_filters(TeamFilter, team_settings)
            init_filters(TeamQAMetricsFilter, team_settings)
            init_predictions_table(TeamPredictionsTable, team_settings)

    @staticmethod
    def post_delete(
        sender: models.Model, instance: models.Model, *args, **kwargs
    ) -> None:
        """ Instance deleting handler. Deletes instance folders.

        Parameters:
        ----------
        sender:
            Object to which the handler should respond.
        instance:
            Instance of Team model.
        """
        instance_dir = get_team_dir(instance)
        shutil.rmtree(instance_dir)

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
post_delete.connect(Team.post_delete, sender=Team)

post_save.connect(User.post_create, sender=User)
post_delete.connect(User.post_delete, sender=User)
