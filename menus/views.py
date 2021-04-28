# Django
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.views import View
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.contrib.auth.mixins import UserPassesTestMixin

# Menus
from .models import (
    Menu,
    MenuOption,
)

# Users
from users.models import MenuOptionSelection
from users.tasks import send_menu_link_to_all_users

# Others
from datetime import datetime


class BasePermissionMixin(UserPassesTestMixin):
    """
    Mixin to limit access to some views to users with the 'add_menu'
    permission. If needed, different permissions could be check for each view,
    like 'view_menu' for the list and detail view, and 'change_menu' for the
    update view.
    """

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.has_perm('menus.add_menu')
        )


class MenuListView(BasePermissionMixin, ListView):
    """
    View for displaying a list of menus by date.
    """
    model = Menu
    ordering = ['date']

    def get_queryset(self):
        # Use prefetch_related to reduce queries
        queryset = super().get_queryset()
        return queryset.prefetch_related('options')


class MenuDetailView(BasePermissionMixin, DetailView):
    """
    View for displaying the detail of a menu.
    """
    model = Menu


class MenuCreateView(BasePermissionMixin, CreateView):
    """
    View for creating a menu.
    """
    model = Menu
    fields = ['date']

    def get_initial(self):
        initial = super().get_initial()
        initial['date'] = datetime.now().date()

        return initial


class MenuUpdateView(BasePermissionMixin, UpdateView):
    """
    View for updating a menu.
    """
    model = Menu
    fields = ['date']


class MenuOptionCreateView(BasePermissionMixin, CreateView):
    """
    View for creating an option for a menu
    """
    model = MenuOption
    fields = ['text']

    def form_valid(self, form):
        # Assign the menu of the pk in kwargs to the created option
        menu = get_object_or_404(Menu, pk=self.kwargs['menu_pk'])
        form.instance.menu = menu
        return super().form_valid(form)


class MenuOptionUpdateView(BasePermissionMixin, UpdateView):
    """
    View for creating an option for a menu
    """
    model = MenuOption
    fields = ['text']


class MenuOptionSelectionListView(BasePermissionMixin, ListView):
    """
    View to list the selection of all users for today's menu
    """
    model = MenuOptionSelection
    ordering = ['user__first_name']
    template_name = 'menus/menuoptionselection_list.html'

    def get_queryset(self):
        # The user can only select the options of today's menu
        menu = get_object_or_404(Menu, date=datetime.now().date())
        queryset = super().get_queryset()
        queryset = queryset.filter(option__menu=menu).select_related(
            'option', 'user',
        )

        return queryset


class SendMenuSelectionLinksView(BasePermissionMixin, View):
    """
    View to send messages with today's menu to all employees (task is sent to
    Celery).
    """

    def post(self, request, *args, **kwargs):
        # Make sure today's menu exists
        get_object_or_404(Menu, date=datetime.now().date())
        send_menu_link_to_all_users.delay(self.request.build_absolute_uri())

        return redirect('menus:menu_list')
