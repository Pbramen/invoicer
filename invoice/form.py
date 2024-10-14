from django import forms
from .models import Invoice, WorkOrder, WorkItem

from django.contrib.auth.models import User
from custom_users.models import Contact, Customer, Address
#from django.forms.models import inlineformset_factory, modelformset_factory, BaseInlineFormSet



class WorkItemForm(forms.ModelForm):
    cost = forms.CharField(required='true', label='Cost', validators=[])
    job_site = forms.ModelChoiceField(queryset=None)

    def __init__(self, contact_id,  *args, **kwargs):
        print('uwu')
        super().__init__(*args, **kwargs)    
        self.fields['job_site'].queryset = Address.objects.filter(
            contact__id = contact_id,
            category='J')
    
    class Meta:
        model = WorkItem
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    invoice_title = forms.CharField(required=True, label='Invoice Title')
    invoice_descript = forms.CharField(required=False, label='Summary')
    deadline = forms.CharField(widget=forms.DateInput(attrs= {'type': 'date'}), required=False)
    status = forms.CharField(required=False)
    work_order = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Invoice
        fields = '__all__'


    def __init__(self, contact, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['work_order'].queryset = WorkOrder.objects.filter(
            vendor_id = contact
        )

'''
    Each child needs their own formset!
    ===================================
    Can we nest this into WorkOrder?

    Parent      ->      Child
  * Invoice     fk      WorkOrder
    Invoice     one     Contact (customer)
    Invoice     one     Contact (issuer)

    WorkOrder   fk      WorkItem
    WorkOrder   one     Contact (vendor) 

    WorkItem    fk      Contact->Address (job site)
'''