from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from custom_users.models import UUIDModel

class WorkOrder(models.Model):
    class StatusTypes(models.TextChoices):
        NOT_ASSIGNED = 'N'
        ASSIGNED = 'A'
        UNDER_REVIEW = 'U'
    
    order_title = models.CharField(max_length=64)
    order_descript = models.CharField(max_length=254)
    vendor = models.ForeignKey('custom_users.Vendor', on_delete=models.CASCADE, related_name='vendor')
    completion_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    job_site = models.ForeignKey('invoice.JobSite', on_delete=models.CASCADE)
    status = models.CharField(choices=StatusTypes, default='N', max_length=1)

    def __str__(self):
        return f'{self.order_title}'


class Invoice(UUIDModel):
    uuid = models.CharField(blank=True, null=False, max_length=16)
    invoice_title = models.CharField(blank=False, max_length=64)
    invoice_descript = models.CharField( max_length=254)
    customer = models.ForeignKey( 'custom_users.Customer', blank=True, null=True, on_delete=models.CASCADE, related_name='recipient')
    issuer = models.ForeignKey("custom_users.UserContactInfo", on_delete=models.CASCADE, related_name='issuer')
    issued_at = models.DateField(auto_now_add=False, editable=True)
    deadline = models.DateField()
    status = models.CharField(default='PENDING', max_length=16)
    work_order = models.ForeignKey(WorkOrder, blank=False, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(uuid_size=16, *args, **kwargs)

    
class JobSite(models.Model):
    address = models.ForeignKey('custom_users.Address', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    

class WorkItem(models.Model):
    validate_money = RegexValidator(regex='[0-9]+\.[0-9]{2}', message='Format must be in 00.00')

    cost = models.FloatField(default=0.00, validators=[validate_money], blank=False)
    memo = models.CharField(null=True, max_length=64)
    descript = models.CharField(null=True, max_length=254)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    

    
class InvoiceAttachment(models.Model):
    upload_file = models.FileField(upload_to="invoice_attachments/%Y/%m/%d/")
    # ffile = models.OneToOneField(FileMeta, on_delete=models.CASCADE)
    # uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=64)
    # descript = models.CharField(max_length=255, blank=True)
    # path = models.CharField(max_length=64)
    # status = models.CharField(max_length=16)
    # work_order = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)

'''
SELECT a.invoice_title, iw.order_title, a.issued_at, a.deadline, b.total from invoice_invoice as a
   JOIN invoice_workorder as iw on iw.id = a.work_order_id
   JOIN (SELECT SUM(cost) as total, work_order_id from invoice_workitem) as b
   on iw.id = b.work_order_id
   WHERE iw.vendor_id = 1;


Select a.invoice_title, a.issued_at, a.deadline, b.total from invoice_invoice 
JOIN invoice_workorder on invoice_workorder.id = a.work_order_id
JOIN 
(SELECT SUM(cost) as total, work_order_id from invoice_workitem
    JOIN invoice_workorder on invoice_workorder.id = invoice_workitem.work_order_id
    GROUP BY invoice_workitem.work_order_id) as b
;
'''