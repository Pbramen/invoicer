from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from custom_users.models import Contact, PhoneNumber
from django import forms

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

class PhoneForm(forms.ModelForm):
    phone_number = forms.CharField(required=True, label="Primary Phone Number")
    cell_types = forms.ChoiceField(required=True, choices=PhoneNumber.CellTypes)
    class Meta:
        model = PhoneNumber
        fields = ('phone_number', 'cell_types')


