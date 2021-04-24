# Django
from django.views.generic.list import ListView

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
    template_name = 'menus/menu_list.html'
    ordering = ['date']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('options')
