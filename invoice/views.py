from django.shortcuts import render, redirect, get_object_or_404

from .form import InvoiceForm,  WorkItemForm
from .models import WorkOrder, WorkItem, Invoice
from custom_users.models import Contact, PhoneNumber, Email, Address
from custom_users.form import PhoneForm, EmailForm, AddressForm

from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.forms import BaseInlineFormSet

@login_required
def index(request):
    partial_template, template_name = 'invoice/index.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
        
    return render(request, template_name, {'partial_template_name': partial_template})

@login_required
def preview(request):
    return render(request, 'invoice/invoice_form.html', {})

@csrf_protect
@login_required
def create(request):
    pass
    #WorkOrderFormSet = modelformset_factory(WorkOrder, form=WorkOrderForm)
    # partial_template, template_name = 'invoicer/formset.html', 'invoicer/base.html'

    # if request.htmx:
    #     template_name = partial_template

    # if request.method == 'POST':
    #     print(list(request.POST.items() ))

    #     workorder_set = WorkOrderFormSet(request.POST, prefix='work_order')
    #     if workorder_set.is_valid():
    #         for form in workorder_set:
    #             print(form.cleaned_data)
    #         pass

    
    # workorder_set = WorkOrderFormSet(prefix='work_order')

    # return render(request, template_name, {
    #     'partial_template_name': partial_template,
    #     'form': workorder_set
    # })

@csrf_protect
@login_required
def create2(request):
    partial_template, template_name = 'invoicer/formset copy.html', 'invoicer/base.html'

    # invoice data
    # PhoneFormSet = modelformset_factory(PhoneNumber, form=PhoneForm, extra=0)
    # EmailFormSet = modelformset_factory(Email, form=EmailForm, extra=0)
    # AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=0)

    # work orders and items
    WorkItemFormSet = inlineformset_factory(WorkOrder, WorkItem, form=WorkItemForm, fields='__all__', extra=0)
  
    print(WorkItemFormSet.form)
    if request.htmx:
        template_name = partial_template
    
    if request.method == 'POST':
        # invoice = InvoiceFormSet(request.POST)
        # phone, email, address = PhoneFormSet(request.POST, prefix="customer_phone"), EmailFormSet(request.POST, prefix="customer_email"), Address(request.POST, prefix='customer_address')
        
        work_items = WorkItemFormSet(request.POST)
        pass

    user = request.user
    u = User.objects.get(username=user).pk
    c = Contact.objects.get(_contact_info__user=u).pk

    work_items = WorkItemFormSet(form_kwargs={'contact_id': c})
    print(work_items)

    # phone, email, address = PhoneFormSet(prefix='customer_phone'), EmailFormSet(prefix='customer_email'), AddressFormSet(prefix="customer_address")
    
    return render(request, template_name, {
        'partial_template_name': partial_template,
        'work_item_form' : work_items
        })

