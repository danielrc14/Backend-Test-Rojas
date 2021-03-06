from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import uuid
import urllib.parse
from .slack_client import send_slack_message


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

    def get_menu_selection_link(self, base_url):
        # String with the link to the view of menu option selection
        return urllib.parse.urljoin(
            base_url,
            reverse(
                'users:menu_selection', args=[str(self.uuid)]
            )
        )

    def send_menu_link_to_slack(self, base_url):
        # Send message to slack with the the link to select an option
        if self.slack_username:
            message = (
                'Follow this link to select your option from today\'s Menu! '
                + self.get_menu_selection_link(base_url)
            )
            if self.slack_username[0] != '@':
                self.slack_username = '@' + self.slack_username
            send_slack_message(message, self.slack_username)


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
