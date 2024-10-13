from django.db import models
from custom_users.models import Contact, Address, Customer
from logger.models import FileMeta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import shortuuid
shortuuid.set_alphabet('23456789BCDGHJKLMPQSTVY')

# Create your models here.
class WorkOrder(models.Model):
    title = models.CharField(max_length=64)
    descript = models.CharField(max_length=254)
    vendor = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='_seller')
    completion_date = models.DateField(auto_now=False, auto_now_add=False)
    

class Invoice(models.Model):
    invoice_uuid = models.CharField(max_length=16)
    title = models.CharField(max_length=64)
    descript = models.CharField( max_length=254)
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='_recipient')
    issuer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='_issuer')
    issued_at = models.DateField()
    deadline = models.DateField()
    status = models.CharField(max_length=16)
    work_orders = models.ManyToManyField(WorkOrder)

    # create a human readable invoice number 
    def generateInvoiceNumber(self, unique=False):
        res = _generateUUID(unique)
        if res:
            self.invoice_uuid = res
        else:
            print('astronomical luck!')
            self.invoice_uuid = 'ASTAR' + res

    def _generateUUID(unique=False):
        if not unique:
            return shortuuid.uuid()[:16]
        
        stop = 5
        uuid = shortuuid.uuid()
        
        # check for dupes
        while len(Invoice.objects.filter(invoice_uuid=uuid)) > 0 and stop > 0:
            uuid = shortuuid.uuid()
            stop -= 1

        return uuid if stop > 0 else None


class WorkItem(models.Model):
    validate_money = RegexValidator(regex='[0-9]+\.[0-9]{2}', message='Format must be in 00.00')
    cost = models.FloatField(default=0.00, validators=[validate_money])
    quantity = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=64)
    descript = models.CharField(max_length=254)
    job_site = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='_job_site')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    

    
class InvoiceAttachment(models.Model):
    pass
    # ffile = models.OneToOneField(FileMeta, on_delete=models.CASCADE)
    # uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=64)
    # descript = models.CharField(max_length=255, blank=True)
    # path = models.CharField(max_length=64)
    # status = models.CharField(max_length=16)
    # work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)

