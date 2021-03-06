from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """
    A model that represents the menu for a specific date.
    """
    date = models.DateField(unique=True)

    def get_absolute_url(self):
        return reverse('menus:menu_detail', args=[str(self.id)])


class MenuOption(models.Model):
    """
    A model that represents a meal option for a menu.
    """
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
