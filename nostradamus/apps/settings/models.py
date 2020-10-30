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


class UserModels(models.Model):
    name = models.CharField(max_length=128)
    model = models.BinaryField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class UserTrainingParameters(models.Model):
    name = models.CharField(max_length=128)
    training_parameters = models.TextField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class UserTopTerms(models.Model):
    top_terms_object = models.BinaryField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class UserBugResolution(models.Model):
    metric = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class UserMarkUpEntity(models.Model):
    name = models.CharField(max_length=128)
    entities = models.TextField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)


class UserSourceField(models.Model):
    name = models.CharField(max_length=128)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)
