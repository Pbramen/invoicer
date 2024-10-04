from django.db import models
from custom_users.models import Contact
from logger.models import FileMeta
from django.contrib.auth.models import User
import uuid
# Create your models here.

class WorkOrder(models.Model):
    title = models.CharField(max_length=64)
    descript = models.CharField(max_length=254)
    seller_id = models.ForeignKey(Contact, on_delete=models.CASCADE)

class Invoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    descript = models.CharField( max_length=254)
    work_order_id = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    issued_at = models.DateField()
    deadline = models.DateField()
    status = models.CharField(max_length=16)


class WorkItem(models.Model):
    work_order_id = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    cost = models.FloatField(default=0.00)
    name = models.CharField(max_length=64)
    descript = models.CharField(max_length=254)
    # do you really need type of work item?

class InvoiceAttachment(models.Model):
    file_id = models.OneToOneField(FileMeta, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Contact, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
    descript = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16)
    work_order_id = models.OneToOneField(WorkOrder, on_delete=models.CASCADE, primary_key=True)

