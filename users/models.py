from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """
    Custom User model to be used instead of the one provided by Django. It
    extends the Django model to add additional fields like the slack username.
    """
    slack_username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )


class MenuOptionSelection(models.Model):
    """
    A model that represents the selection of a user between the options of a
    menu
    """
    option = models.ForeignKey(
        'menus.MenuOption',
        related_name='selections',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='selections',
        on_delete=models.CASCADE,
    )
    preferences = models.TextField(
        blank=True,
        null=True,
    )
