# Django
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied

# Models
from .models import (
    User,
    MenuOptionSelection,
)
from menus.models import Menu

# Forms
from .forms import MenuOptionSelectionForm

# Others
from datetime import (
    datetime,
    time,
)


class SelectMenuOptionView(FormView):
    """
    View for a user to select his option for today's menu.
    """
    model = MenuOptionSelection
    form_class = MenuOptionSelectionForm
    template_name = 'menu_selection/menu_selection_today.html'

    def dispatch(self, *args, **kwargs):
        self.user = get_object_or_404(User, uuid=self.kwargs.get('uuid'))
        # Forbid users to select an option after 11:00
        if datetime.now().time() > time(hour=11):
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """
        Get today's menu and the user's selection (if it exists), and pass
        them to the form
        """
        kwargs = super().get_form_kwargs()
        menu = get_object_or_404(Menu, date=datetime.now().date())
        selection = MenuOptionSelection.objects.filter(
            user=self.user,
            option__menu=menu,
        ).first()
        kwargs['instance'] = selection
        kwargs['menu'] = menu

        return kwargs

    def form_valid(self, form):
        # Assign user to the instance and save it
        form.instance.user = self.user
        form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:menu_selection', args=[str(self.user.uuid)])
