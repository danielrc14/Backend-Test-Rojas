# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import (
    Permission,
    Group,
)

# Models
from users.models import User
from menus.models import (
    Menu,
    MenuOption,
)

# Others
from datetime import (
    datetime,
    timedelta,
)


class MenusTestCase(TestCase):
    def setUp(self):
        """
        Set up users, permissions, and other objects
        """
        group = Group.objects.create(name='test_group')
        permission = Permission.objects.get(codename='add_menu')
        group.permissions.add(permission)

        self.user_without_permission = User.objects.create(
            email='withoutpermission@test.cl', username='withoutpermission',
        )
        self.user_with_permission = User.objects.create(
            email='withpermission@test.cl', username='withpermission',
        )
        self.user_without_permission.set_password('test')
        self.user_with_permission.set_password('test')
        self.user_without_permission.save()
        self.user_with_permission.save()
        self.user_with_permission.groups.add(group)
        self.setup_menu = Menu.objects.create(
            date=datetime.now().date() - timedelta(days=1)
        )

    def login(self, username, password):
        login_url = reverse('login')
        self.client.post(
            login_url, {
                'username': username,
                'password': password,
            }
        )

    def test_permissions(self):
        """
        Test views permission restrictions are working properly (all restricted
        views use the same mixin, so only one of them is tested)
        """
        url = reverse('menus:menu_list')

        # Test user without permission
        self.login('withoutpermission', 'test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Test user with permission
        self.login('withpermission', 'test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_menu_create_update(self):
        """
        Test creation and update of a menu
        """
        self.login('withpermission', 'test')

        # Test create
        create_url = reverse('menus:menu_create')
        date = datetime.now().date()
        self.client.post(create_url, {'date': date})
        menu = Menu.objects.filter(date=date).first()
        self.assertTrue(menu is not None)

        # Test update
        update_url = reverse('menus:menu_update', args=[str(menu.id)])
        date = datetime.now().date() + timedelta(days=1)
        self.client.post(update_url, {'date': date})
        menu = Menu.objects.get(id=menu.id)
        self.assertEqual(menu.date, date)

    def test_menu_option_create_update(self):
        """
        Test creation and update of menu options
        """
        self.login('withpermission', 'test')

        # Test create
        create_url = reverse(
            'menus:menuoption_create',
            args=[str(self.setup_menu.id)],
        )
        option_text = 'test option'
        self.client.post(create_url, {'text': option_text})
        option = MenuOption.objects.filter(
            menu=self.setup_menu,
            text=option_text,
        ).first()
        self.assertTrue(option is not None)

        # Test update
        update_url = reverse(
            'menus:menuoption_update',
            args=[str(option.id)],
        )
        option_text = 'test option 2'
        self.client.post(update_url, {'text': option_text})
        option = MenuOption.objects.get(id=option.id)
        self.assertEqual(option.text, option_text)

    # TODO: test slack integration
