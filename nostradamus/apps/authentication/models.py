from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)

    REQUIRED_FIELDS = ("name", "email", "password")

    class Meta:
        verbose_name = "User"
        db_table = "users"

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
