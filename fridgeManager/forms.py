from django import forms
from fridgeManager.models import food_item, UserProfile,food_category,food_item,FridgeFoodItem
from django.contrib.auth.models import User


class new_food_item_form(forms.ModelForm):

    class Meta:
        model = food_item
        exclude = ()

class create_category_form(forms.ModelForm):

    class Meta:
        model = food_category
        exclude = ()

class add_to_fridge_form(forms.ModelForm):

    class Meta:
        model = FridgeFoodItem
        exclude = ()



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label="Phone number", required=False)

    class Meta:
        model = UserProfile
        fields = ('phone_number',)
