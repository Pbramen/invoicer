
from custom_users.models import UserContactInfo, Vendor, Customer
from invoice.models import WorkOrder
from django.shortcuts import get_object_or_404
from typing import Optional, TypedDict

class OrderByOptions(TypedDict):
    field: str
    asc: bool


# param (user) - String username
def get_vendor_by_employee(user:str):
    user_contact = get_object_or_404(UserContactInfo, user__username=user).contact
    return Vendor.objects.get(employees__employee=user_contact)

# param (vendor) - vendor queryset
# returns WorkOrder queryset 
def get_work_orders_by_vendor(vendor:Vendor, status='N', orderBy: Optional[OrderByOptions] =  None):
    return WorkOrder.objects.filter(vendor=vendor, status = status).order_by('id')

# param (vendor) - vendor queryset
# returns Customer queryset
def get_customers_by_vendor(vendor:Vendor):
    return Customer.objects.filter(vendor_to_customer__vendor=vendor.pk)

