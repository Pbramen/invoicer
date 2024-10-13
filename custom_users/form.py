from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from custom_users.models import Contact, PhoneNumber, Address, Email
from django import forms

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

class PhoneForm(forms.ModelForm):
    phone_number = forms.CharField(required=True, label="Primary Phone Number", validators=[PhoneNumber.validate_phone])
    category = forms.ChoiceField(required=True, label="Type", choices=PhoneNumber.CellTypes)
    class Meta:
        model = PhoneNumber
        fields = ('phone_number', 'category')
        
class AddressForm(forms.ModelForm):
    street = forms.CharField(required=True, label="Street Address")
    state = forms.ChoiceField(required=True, label='State', choices=Address.StateAbbr)
    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zipcode')

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email Address")
    class Meta:
        model = Email
        fields = ('email',)

