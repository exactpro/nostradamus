from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.authentication.models import User


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_settings"
        managed = False


class UserFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    type = models.CharField(
        max_length=128,
        choices=FiltrationTypes.choices,
        default=FiltrationTypes.STRING,
    )
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_filter"
        managed = False


class UserQAMetricsFilter(models.Model):
    class FiltrationTypes(models.TextChoices):
        STRING = "string", _("String")
        DROP_DOWN = "drop-down", _("Drop-down")
        NUMERIC = "numeric", _("Numeric")
        DATE = "date", _("Date")

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=FiltrationTypes.choices)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_qa_metrics_filter"
        managed = False


class UserPredictionsTable(models.Model):
    name = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)
    position = models.IntegerField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_predictions_table"
        managed = False


class UserModels(models.Model):
    name = models.CharField(max_length=128)
    model = models.BinaryField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_models"


class UserTrainingParameters(models.Model):
    name = models.CharField(max_length=128)
    training_parameters = models.TextField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_training_parameters"


class UserTopTerms(models.Model):
    top_terms_object = models.BinaryField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_top_terms"


class UserBugResolution(models.Model):
    metric = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_bug_resolution"


class UserMarkUpEntity(models.Model):
    name = models.CharField(max_length=128)
    entities = models.TextField()
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_mark_up_entity"


class UserSourceField(models.Model):
    name = models.CharField(max_length=128)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_source_field"
