from django.db import models
from django.contrib.auth.models import User


class MenuOptionSelection(models.Model):
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
