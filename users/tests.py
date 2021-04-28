# Django
from django.test import TestCase
from django.urls import reverse

# Models
from users.models import (
    User,
    MenuOptionSelection,
)
from menus.models import (
    Menu,
    MenuOption,
)

# Others
from datetime import (
    datetime,
    date,
)
from freezegun import freeze_time

"""
- Test queryset of MenuOptionSelectionForm???
- Post to SelectMenuOptionView without selection and with selection
- Time restrictions
"""


class UsersTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test.cl', username='test',
        )
        self.setup_menu = Menu.objects.create(date=date(2021, 1, 1))
        self.option1 = MenuOption.objects.create(
            menu=self.setup_menu,
            text='Option 1',
        )
        self.option2 = MenuOption.objects.create(
            menu=self.setup_menu,
            text='Option 2',
        )

    @freeze_time('2021-01-01 10:00:00')
    def test_within_time_limits(self):
        url = reverse(
            'users:menu_selection',
            args=[str(self.user.uuid)],
        )

        # Test create
        response = self.client.post(url, {'option': self.option1.id})
        self.assertEqual(response.status_code, 302)
        selection = MenuOptionSelection.objects.filter(
            user=self.user,
            option__menu=self.setup_menu,
        ).first()
        self.assertTrue(selection is not None)
        self.assertEqual(selection.option, self.option1)

        # Test update
        response = self.client.post(url, {'option': self.option2.id})
        self.assertEqual(response.status_code, 302)
        selection_queryset = MenuOptionSelection.objects.filter(
            user=self.user,
            option__menu=self.setup_menu,
        )
        self.assertEqual(selection_queryset.count(), 1)
        selection = MenuOptionSelection.objects.get(id=selection.id)
        self.assertEqual(selection.option, self.option2)

    @freeze_time('2021-01-01 12:00:00')
    def test_out_of_time_limits(self):
        url = reverse(
            'users:menu_selection',
            args=[str(self.user.uuid)],
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
