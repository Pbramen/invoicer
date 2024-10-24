from django import forms
from .models import Invoice, WorkItem
from custom_users.models import Vendor
from .queries import get_work_orders_by_vendor, get_customers_by_vendor

class WorkItemForm(forms.ModelForm):
    cost = forms.FloatField(required=True, label='Amount', min_value=0, widget=forms.NumberInput(attrs={'step': '0.01'}))    
    memo = forms.CharField(required=False)
    descript = forms.CharField(required=False, label='Item Description', widget=forms.Textarea(attrs={'rows': '2'}))
    class Meta:
        model = WorkItem
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    invoice_title = forms.CharField(required=True, label='Invoice Title', widget=forms.TextInput(attrs={'required': 'required'}))
    invoice_descript = forms.CharField(required=False, label='Summary', widget=forms.Textarea(attrs={'rows': '2'}))
    issued_at = forms.DateField(widget=forms.DateInput( attrs={'type': 'date'}))
    deadline = forms.CharField(widget=forms.DateInput( attrs= {'type': 'date'}), required=False)
    status = forms.CharField(required=False)
    work_order = forms.ModelChoiceField(required=True, queryset=None, label="Select one Work Order", widget=forms.Select(attrs={'required': 'required'}) ) 
    customer = forms.ModelChoiceField(required=False, queryset=None, label="Select pre-existing customer")
    
    class Meta:
        model = Invoice
        fields = ('invoice_title', 'invoice_descript', 'issued_at', 'deadline', 'status', 'work_order', 'customer')

    def __init__(self, vendor:Vendor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_order'].queryset = get_work_orders_by_vendor(vendor=vendor)
        self.fields['customer'].queryset = get_customers_by_vendor(vendor=vendor)
        
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        print(cleaned_data)
        
        # if len(temp) == 3:
        #     self.deadline = f"{temp[2]}-{temp[0]}-{temp[1]}"
        # else:
        #     raise ValidationError('Unable to convert datefield to YYYY-MM-DD format.')        
        return cleaned_data

