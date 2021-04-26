from django import forms
from .models import MenuOptionSelection


class MenuOptionSelectionForm(forms.ModelForm):
    """
    Form to create and update a menu option selection
    """

    class Meta:
        model = MenuOptionSelection
        fields = ('option', 'preferences')

    def __init__(self, *args, **kwargs):
        # Reduce the options queryset to the menu's options
        menu = kwargs.pop('menu')
        super().__init__(*args, **kwargs)
        if menu:
            self.fields['option'].queryset = self.fields['option'].queryset\
                .filter(menu=menu)
