from django import forms
from .models import MenuItem, Category


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        menu_items = [(c.id, c.get_menu_items()) for c in categories]

        self.fields['category'].choices = menu_items
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'