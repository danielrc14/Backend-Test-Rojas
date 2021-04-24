from django.db import models
from django.contrib.auth.models import User


# TODO: docstrings???

class Menu(models.Model):
    date = models.DateField()


class MenuOption(models.Model):
    menu = models.ForeignKey(
        Menu,
        related_name='menu',
        on_delete=models.CASCADE,
    )
    text = models.TextField()


class MenuOptionSelection(models.Model):
    option = models.ForeignKey(
        MenuOption,
        related_name='menu_option',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
    )
    preferences = models.TextField(
        blank=True,
        null=True,
    )
