from django import forms
from fridgeManager.models import food_item


class new_food_item_form(forms.ModelForm):

    class Meta:
        model = food_item
        exclude = ()