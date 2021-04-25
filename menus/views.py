# Django
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.shortcuts import get_object_or_404

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


class MenuOptionCreateView(CreateView):
    """
    View for creating an option for a menu
    """
    model = MenuOption
    fields = ['text']

    def form_valid(self, form):
        menu = get_object_or_404(Menu, pk=self.kwargs['menu_pk'])
        form.instance.menu = menu
        return super().form_valid(form)


class MenuOptionUpdateView(UpdateView):
    """
    View for creating an option for a menu
    """
    model = MenuOption
    fields = ['text']
