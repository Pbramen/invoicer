from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

def createNewUser(user, phone):
    contact_obj = Contact.objects.create(name=f"{user.cleaned_data['first_name']} {user.cleaned_data['last_name']}")
    contact_obj.save()
    user_obj = user.save()
    Customer.objects.create(user_id=user_obj, contact_id=contact_obj )

    phone.save(commit=False)
    phone.contact_id = contact_obj.pk

    phone.save()
    print('user registration success')


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class PhoneNumber(models.Model):
    class CellTypes(models.TextChoices):
        MOBILE = "M"
        HOME = "H"
        WORK = "W"
        OTHER = "O"

    cell_type = models.CharField(max_length=8, choices=CellTypes, default=CellTypes.MOBILE)
    phone_number = models.CharField(max_length=12)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.value}"


class EmailAddresse(models.Model):
    type = models.CharField(max_length=12)
    value = models.CharField(max_length=254)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.value}"

class PhysicalAddresse(models.Model):
    type = models.CharField(max_length=12)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=16)
    zipcode = models.CharField(max_length=12) #ZIP+4 ~ 9 characters long for US 
    lat = models.FloatField()
    lng = models.FloatField()
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

# intermmediary table for users and contact information
class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    default_alert = models.CharField(db_comment="Time before due date when email notification is sent",max_length=24)
    
# TODO: make a custom user account.
