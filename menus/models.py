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

    def __str__(self):
        return self.text
