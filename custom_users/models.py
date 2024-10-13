from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from invoicer import abstract_models


class PhoneNumber(abstract_models.RemoveWS_Model):
    phone_format = 'xxx xxx-xxxx'
    phone_regex = '^[0-9]{3} [0-9]{3}-[0-9]{4}$'
    validate_phone = RegexValidator(regex=phone_regex, message=f"Phone number must be in the format ${phone_format}.")

    
    class CellTypes(models.TextChoices):
        MOBILE = "M"
        HOME = "H"
        WORK = "W"
        OTHER = "O"

    category = models.CharField(max_length=1, choices=CellTypes, default=CellTypes.MOBILE)
    phone_number = models.CharField(max_length=12, validators=[validate_phone])
    
    def __str__(self):
        return f"Phone Number: ({self.category}) {self.value}"
    

class Email(abstract_models.RemoveWS_Model):
    class EmailTypes(models.TextChoices):
        PERSONAL = 'P'
        WORK = 'W'
        ALTERNATIVE = 'A'
        OTHER = 'O'

    category = models.CharField(max_length=1, choices=EmailTypes, default=EmailTypes.PERSONAL)
    email = models.EmailField(max_length=254)


    def __str__(self):
        return f"email: ({self.category}) {self.email}"

 
class Address(abstract_models.RemoveWS_Model):
    
    class StateAbbr(models.TextChoices):
        ALABAMA = "AL"
        KENTUCKY = "KY"
        OHIO = "OH"
        ALASKA = "AK" 
        LOUISIANA = "LA"
        OKLAHOMA = "OK"
        ARIZONA = "AZ"
        MAINE = "ME"
        OREGON = "OR"
        ARKANSAS = "AR"
        MARYLAND = "MD"
        PENNSYLVANIA = "PA"
        MASSACHUSETTS = "MA"
        NEW_HAMPSHIRE = "NH"
        CALIFORNIA = "CA"
        MICHIGAN = "MI"
        RHODE_ISLAND = "RI"
        COLORADO = "CO"
        MINNESOTA = "MN"
        SOUTH_CAROLINA = "SC"
        CONNECTICUT = "CT"
        MISSISSIPPI = "MS"
        SOUTH_DAKOTA = "SD"
        DELAWARE = "DE"
        MISSOURI = "MO"
        TENNESSEE = "TN"
        MONTANA = "MT"
        TEXAS = "TX"
        FLORIDA = "FL"
        NEBRASKA = "NE"
        GEORGIA = "GA"
        NEVADA = "NV"
        UTAH = "UT"
        VERMONT = "VT"
        HAWAII = "HI"
        NEW_JERSEY = "NJ"
        VIRGINIA = "VA"
        IDAHO = "ID"
        NEW_MEXICO = "NM"
        ILLINOIS = "IL"
        NEW_YORK = "NY"
        WASHINGTON = "WA"
        INDIANA = "IN"
        NORTH_CAROLINA = "NC"
        WEST_VIRGINIA = "WV"
        IOWA = "IA"
        NORTH_DAKOTA = "ND"
        WISCONSIN = "WI"
        KANSAS = "KS"
        WYOMING = "WY"

    class CategoryTypes(models.TextChoices):
        JOB_SITE = 'J'
        HOME = 'M'
        COMPANY = 'C'
        OTHER = 'O'

    
    validate_zipcode = RegexValidator(regex='^[0-9]{5}(-[0-9]{4})?$', message="Invalid zipcode format")
    
    category = models.CharField(max_length=12, choices=CategoryTypes, blank=True, null=True, default='M')
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=2, choices=StateAbbr, default=StateAbbr.ALABAMA)
    zipcode = models.CharField(max_length=12, validators=[]) #ZIP+4 ~ 9 characters long for US 

    # query geolocation api for this information?
    # if we have permission, then when searching for addresses that are already registered, we can look up by lat and lng instead
    lat = models.FloatField(blank=True, null=True, default=None)
    lng = models.FloatField(blank=True, null=True, default=None)

    def __str__(self):
        return f"address: {self.street} {self.city}, {self.state}"

        
########################################################################

# Create your models here.
class Contact(abstract_models.RemoveWS_Model):
    name = models.CharField(max_length=128)
    phoneNumber = models.ManyToManyField(PhoneNumber)
    email = models.ManyToManyField(Email)
    address = models.ManyToManyField(Address)
    
    def __str__(self):
        return f"{self.name}"


# intermmediary table for users and contact information
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, related_name='_contact')
    default_alert = models.CharField(default='30d', db_comment="Time before due date when email notification is sent",max_length=24)
    vendor_to_customer = models.ManyToManyField(Contact, through="VendorCustomer")


class VendorCustomer(models.Model):
    vendor = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='_vendor')
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='_vendor_customer')
    date_created = models.DateField(auto_now=False, auto_now_add=True, editable=False)
     


########################################################################

def createNewUser(user, phone, address):
    full_name = ''
    if user.cleaned_data['first_name'] and user.cleaned_data['last_name']:
        full_name = f"{user.cleaned_data['first_name']} {user.cleaned_data['last_name']}"
    
    contact_obj = Contact.objects.create(name=full_name)
    Customer.objects.create(user=user.save(), contact=contact_obj)
    
    a1, _ = Address.objects.get_or_create(
        street=address.cleaned_data['street'],
        city=address.cleaned_data['city'],
        state=address.cleaned_data['state'],
        zipcode=address.cleaned_data['zipcode']
    )
    p1, _ = PhoneNumber.objects.get_or_create(
        category=phone.cleaned_data['category'],
        phone_number=phone.cleaned_data['phone_number']
    )

    contact_obj.address.add(a1)
    contact_obj.phoneNumber.add(p1)