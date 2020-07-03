from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.authentication.models import Team, User


class TeamSettings(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TeamFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    filtration_type = models.CharField(
        max_length=128,
        choices=FiltrationTypes.choices,
        default=FiltrationTypes.STRING,
    )
    settings = models.ForeignKey(TeamSettings, on_delete=models.CASCADE)


class UserFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    filtration_type = models.CharField(
        max_length=128,
        choices=FiltrationTypes.choices,
        default=FiltrationTypes.STRING,
    )
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class TeamQAMetricsFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    filtration_type = models.CharField(
        max_length=128, choices=FiltrationTypes.choices
    )
    settings = models.ForeignKey(TeamSettings, on_delete=models.CASCADE)


class UserQAMetricsFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    filtration_type = models.CharField(
        max_length=128, choices=FiltrationTypes.choices
    )
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class TeamPredictionsTable(models.Model):
    name = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)
    position = models.IntegerField()
    settings = models.ForeignKey(TeamSettings, on_delete=models.CASCADE)


class UserPredictionsTable(models.Model):
    name = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)
    position = models.IntegerField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)
