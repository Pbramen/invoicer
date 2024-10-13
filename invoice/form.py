from django import forms
from .models import Invoice, WorkOrder, WorkItem
#from django.forms.models import inlineformset_factory, modelformset_factory, BaseInlineFormSet

class WorkOrderForm(forms.ModelForm):
    descript = forms.CharField(widget=forms.Textarea, max_length=254, required=False)
    class Meta:
        model = WorkOrder
        fields = ('title', 'descript')


class WorkItemForm(forms.ModelForm):
    cost = forms.CharField(required='true', label='Cost', validators=[])
    class Meta:
        model = WorkItem
        fields = ('name', 'descript', 'cost', 'quantity')

class InvoiceForm(forms.ModelForm):
    title = forms.CharField(required=True, label='Invoice Title')
    descript = forms.CharField(required=False, label='Summary')
    deadline = forms.CharField(widget=forms.DateInput(attrs= {'type': 'date'}), required=False)
    status = forms.CharField(required=False)
    
    
    class Meta:
        model = Invoice
        fields = ('title', 'descript', 'deadline', 'status')


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