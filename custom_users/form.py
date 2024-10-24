from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from custom_users.models import PhoneNumber, Address, Email, Vendor, Customer
from django import forms
import re


def noWS(value):
    return re.sub(r'[ \t\r\n]{2,}', ' ', value).strip() == value

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

class RegisterVendor(forms.ModelForm):
    vendor_name = forms.CharField(max_length='32', label='Company/Vendor Name', required=True)
    class Meta:
        model = Vendor
        fields = ('vendor_name', )


class CustomerForm(forms.ModelForm):
    customer_name = forms.CharField(max_length='32', label='Customer Name', required='True')
    class Meta:
        model=Customer
        fields = ('customer_name',)

    
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

phoneFormset = forms.modelformset_factory(PhoneNumber, form=PhoneForm, fields=('phone_number', 'category'), can_delete=False, extra=0)
addressFormset = forms.modelformset_factory(Address, form=AddressForm, fields=('street', 'city', 'state', 'zipcode'), can_delete=False, extra=0)
emailFormset = forms.modelformset_factory(Email, fields=('email',), form=EmailForm, can_delete=False, extra=0)
