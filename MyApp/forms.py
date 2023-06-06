from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfileModel, InputModel
from django.core.exceptions import ValidationError


# Create your forms here.


class NewUserForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfileModel
        fields = ("username", "email", "phone_number")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateProfileForm(UserChangeForm):

    class Meta:
        model = UserProfileModel
        fields = ("username", "email", "phone_number", "gender", "first_name", "middle_name", "last_name", "tokens", "access_level", "uid")


class InputForm(forms.ModelForm):

    class Meta:
        model = InputModel
        fields = ['input_user', 'user']
        #widgets = {'user': forms.HiddenInput()}
