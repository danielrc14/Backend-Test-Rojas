from django import forms
from .models import MenuOptionSelection


class MenuOptionSelectionForm(forms.ModelForm):

    class Meta:
        model = MenuOptionSelection
        fields = ('option', 'preferences')

    def __init__(self, *args, **kwargs):
        menu = kwargs.pop('menu')
        super().__init__(*args, **kwargs)
        if menu:
            self.fields['option'].queryset = self.fields['option'].queryset\
                .filter(menu=menu)
