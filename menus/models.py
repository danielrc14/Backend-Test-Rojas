from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# TODO: docstrings???

class Menu(models.Model):
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('menus:menu_detail', args=[str(self.id)])


class MenuOption(models.Model):
    menu = models.ForeignKey(
        Menu,
        related_name='options',
        on_delete=models.CASCADE,
    )
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('menus:menu_detail', args=[str(self.menu.id)])


class MenuOptionSelection(models.Model):
    option = models.ForeignKey(
        MenuOption,
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
