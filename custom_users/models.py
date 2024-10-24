from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from invoicer import abstract_models

import shortuuid

alphabeat = '23456789BCDGHJKLMPQSTVY'
shortuuid.set_alphabet(alphabeat)

class UUIDModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.CharField(max_length=22, editable=False, blank=True)
    
    @classmethod
    def generateUUID(cls, size):
        stop = 10
        uuid = shortuuid.uuid()[:size]
        
        # check for dupes
        while stop > 0:
            if cls.objects.filter(uuid=uuid).count() == 0:
                return uuid
            stop -=1
            uuid = shortuuid.uuid()[:size]

        raise ValidationError('Failed to generate unique identifer after 10 cycles.')

    def save(self, uuid_size=22, *args, **kwargs):
        # generate if uuid does not exist yet.
        if not self.uuid or self.uuid == 0:
            self.uuid = self.generateUUID(size=uuid_size)
        super().save(*args, **kwargs)



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
        return f"Phone Number: ({self.category}) {self.phone_number}"
    

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
    
    category = models.CharField(max_length=12, choices=CategoryTypes, null=True, default='M')
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=2, choices=StateAbbr, default=StateAbbr.ALABAMA)
    zipcode = models.CharField(max_length=12, validators=[]) #ZIP+4 ~ 9 characters long for US 

    # query geolocation api for this information?
    # if we have permission, then when searching for addresses that are already registered, we can look up by lat and lng instead
    lat = models.FloatField( null=True, default=None)
    lng = models.FloatField( null=True, default=None)

    def __str__(self):
        return f"{self.street} {self.city}, {self.state} {self.zipcode}"

        
########################################################################

class Contact(abstract_models.RemoveWS_Model):
    name = models.CharField(max_length=128)
    phoneNumber = models.ManyToManyField(PhoneNumber)
    email = models.ManyToManyField(Email)
    address = models.ManyToManyField(Address)
    
    def __str__(self):
        return f"{self.name}"


class Employees(models.Model):
    class EmployeeRoleTypes(models.TextChoices):
        EMPLOYEE = 'E'
        ADMIN = 'A'

    employee =  models.OneToOneField("custom_users.Contact", on_delete=models.CASCADE)
    vendor = models.ForeignKey('custom_users.Vendor', on_delete=models.CASCADE)
    role = models.CharField( default=EmployeeRoleTypes.EMPLOYEE, max_length=1)


class Vendor(UUIDModel):
    vendor_name = models.CharField(max_length=64)
    vendor_contact = models.ForeignKey("custom_users.Contact" , blank=True, on_delete=models.CASCADE, related_name='vendor_contact')
    status = models.BooleanField(default=True)

    def save(self, uuid_size=16, *args, **kwargs):
        super().save(uuid_size=uuid_size, *args, **kwargs)
        

class Customer(models.Model):
    customer_name = models.CharField(max_length=64)
    customer_contact = models.ForeignKey("custom_users.Contact", on_delete=models.CASCADE)
    is_registered = models.BooleanField()
    vendor_to_customer = models.ManyToManyField("custom_users.Vendor", through='custom_users.VendorCustomer')

    def __str__(self):
        return f'${self.customer_name}'


class VendorCustomer(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_LUT')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_LUT')
    date_created = models.DateField(auto_now=False, auto_now_add=True, editable=False)


# intermmediary tables
class UserContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='user_contact')
    alert_timeframes = models.CharField(default='30d', db_comment="Time before due date when email notification is sent", max_length=24)


########################################################################
from typing import Optional
from custom_users.form import CustomerForm
from .form import PhoneForm, EmailForm, AddressForm, RegisterVendor
def saveContact(contact: UserContactInfo, phone: Optional[PhoneForm]=None, address:Optional[AddressForm]=None, addr_cat:Optional[str]='M', email: Optional[EmailForm]=None, email_cat:Optional[str]='P'): 
    if address: 
        a1, _ = Address.objects.get_or_create(
                    street=address.cleaned_data['street'],
                    city=address.cleaned_data['city'],
                    state=address.cleaned_data['state'],
                    zipcode=address.cleaned_data['zipcode'],
                    category=addr_cat
                )    
        contact.address.add(a1)
    if phone: 
        p1, _ = PhoneNumber.objects.get_or_create(
                    category=phone.cleaned_data['category'],
                    phone_number=phone.cleaned_data['phone_number']
                )
        contact.phoneNumber.add(p1)
    if email: 
        pass
        #e1, _ = Email.objects.get_or_create()

def createNewUser(user, phone, address):
    full_name = ''
    if user.cleaned_data['first_name'] and user.cleaned_data['last_name']:
        full_name = f"{user.cleaned_data['first_name'].capitalize()} {user.cleaned_data['last_name'].capitalize()}"
    
    user_obj = user.save()
    user_obj.groups.add(Group.objects.get(name='customer'))
    
    contact_obj = Contact.objects.create(name=full_name)
    UserContactInfo.objects.create(user=user_obj, contact=contact_obj)
    
    saveContact(contact_obj, phone, address)
    return {'user': user_obj, 'contact': contact_obj}

def createCompany(user_contact:Contact, vendor:RegisterVendor, phone:PhoneForm, address:AddressForm, email:Email):
    
    v_instance = vendor.save(commit=False)
    vendor_contact = Contact.objects.create(name=v_instance.vendor_name)

    v_instance.vendor_contact = vendor_contact
    v_instance.save()
    
    saveContact(contact=vendor_contact, phone=phone, address=address, addr_cat='J', email=email)
    Employees.objects.create(employee=user_contact, vendor=v_instance, role='A')
    pass


def createCustomer(customer: CustomerForm, phone:Optional[PhoneForm]=None, email:Optional[AddressForm]=None, address:Optional[AddressForm]=None):
    # create customer -> set is registered to false 
    customer_obj = customer.save(commit=False)
    # create contact 
    contact = Contact.objects.create(name=customer_obj.customer_name)
    customer_obj.customer_contact = contact
    customer_obj.is_registered = False
    customer_obj.save()

    # save all formsets 
    contact.phoneNumber.add(phone.save())
    contact.address.add(address.save())
    contact.email.add(email.save()) 
    return customer_obj