# Django
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)

# Models
from .models import (
    Menu,
    MenuOption,
    MenuOptionSelection,
)


class MenuListView(ListView):
    """
    View for displaying a list of menus by date.
    """
    model = Menu
    ordering = ['date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('options')


class MenuDetailView(DetailView):
    """
    View for displaying the detail of a menu.
    """
    model = Menu


class MenuCreateView(CreateView):
    """
    View for creating a menu.
    """
    model = Menu
    fields = ['date']


class MenuUpdateView(UpdateView):
    """
    View for updating a menu.
    """
    model = Menu
    fields = ['date']
