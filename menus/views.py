# Django
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin

# Models
from .models import (
    Menu,
    MenuOption,
    MenuOptionSelection,
)


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
        menu = get_object_or_404(Menu, pk=self.kwargs['menu_pk'])
        form.instance.menu = menu
        return super().form_valid(form)


class MenuOptionUpdateView(BasePermissionMixin, UpdateView):
    """
    View for creating an option for a menu
    """
    model = MenuOption
    fields = ['text']
