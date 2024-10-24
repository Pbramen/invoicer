from django.shortcuts import render, redirect

from .form import InvoiceForm,  WorkItemForm
from .models import WorkOrder, WorkItem
from .queries import get_vendor_by_employee

from custom_users.models import UserContactInfo, VendorCustomer, Vendor, createCustomer, alphabeat

from django.db import transaction
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from custom_users.form import CustomerForm, PhoneForm, EmailForm, AddressForm
# Create your views here.
from django.views.decorators.http import require_http_methods
from django.views import generic

from django.db import connection

WorkItemFormSet = modelformset_factory(WorkItem, form=WorkItemForm, exclude=('work_order',),can_delete=False, extra=1)
#InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, exclude=('issuer', 'invoice_uuid'), can_delete=False, extra=1)

@transaction.atomic
@csrf_protect
@login_required(login_url='/user/login/')
@permission_required('invoice.add_invoice', raise_exception=True)
def create(request):
    partial_template, template_name = 'invoicer/formset copy.html', 'invoicer/base.html'
    print('create endpoint reached')
    if request.htmx:
        template_name = partial_template

    # grab the contact_id to filter choices
    vendor = get_vendor_by_employee(request.user)
    resubmit=False
    
    if request.method == 'POST':
        print('post request recieved')
        active_tab = request.POST.get('activate_tab')
        if not active_tab or active_tab not in ['select_customer', 'create_customer']:
            active_tab = "select_customer"

        invoice_order = InvoiceForm(data = request.POST, vendor=vendor, prefix='invoice_order')
        work_items = WorkItemFormSet(data = request.POST, prefix='item')

        
        customer = CustomerForm(request.POST, prefix='c')
        customer_phone = PhoneForm(request.POST, prefix='c_phone')
        customer_address = AddressForm(request.POST, prefix='c_address')
        customer_email = EmailForm(request.POST, prefix='c_email')


        if  invoice_order.is_valid() and        \
            work_items.is_valid() and           \
            customer_address.is_valid() and     \
            customer_phone.is_valid() and       \
            customer_email.is_valid() and       \
            customer.is_valid():
            
            invoice = invoice_order.save(commit=False)
            
            if customer:
                print('creating new customer...')
                invoice.customer = createCustomer(customer, phone=customer_phone, email=customer_email, address=customer_address)
                VendorCustomer.objects.create(customer=invoice.customer, vendor=vendor)
            c = UserContactInfo.objects.get(user__username=request.user)
    
            invoice.issuer = c
            invoice.save()
    
            work_order_id = WorkOrder.objects.get(pk = invoice.work_order.id)
            work_order_id.status = 'A'
            items = work_items.save(commit=False)
        
            for item in items:
                print(item)
                item.work_order = work_order_id
            work_items.save()
            print('success!')
            return redirect('/invoice/')
      
        else:
            print('error triggered...')
            if customer.errors or customer_address.errors or customer_email.errors or customer_phone.errors:
                active_tab = "create_customer"
            resubmit=True
    else:
        # reset the form on get
        work_items = WorkItemFormSet(queryset=WorkItem.objects.none(), prefix='item')
        invoice_order = InvoiceForm(vendor=vendor, prefix='invoice_order')
        
        active_tab = "select_customer"
        customer = CustomerForm(prefix='c')
        customer_phone = PhoneForm(prefix='c_phone')
        customer_address = AddressForm(prefix='c_address')
        customer_email = EmailForm(prefix='c_email')


       
    return render(request, template_name, {
        'partial_template_name': partial_template,
        'work_item_form' : work_items,
        'invoice_form' : invoice_order,
        'resubmit' : resubmit,
        'customer' : customer,
        'customer_addr_form' : customer_address,
        'customer_email_form' : customer_email,
        'customer_phone_form' : customer_phone,
        'active_tab' : active_tab
        }
    )

from custom_users.models import Contact, Employees, Customer

def get_invoice(user: str, uuid:str):

    # TODO: CTE or View to make this more maintainable OR denormalize db.
    sql = "Select a.invoice_title, a.invoice_descript, a.deadline, a.status, d.customer_name, \
        addr.street, addr.city, addr.state, addr.zipcode, addr.category, \
        email.email, email.category,\
        phone.phone_number, phone.category, \
        v.vendor_name, addr_v.street, addr_v.city, addr_v.state, addr_v.zipcode, addr_v.category, \
        email_v.email, email_v.category,\
        phone_v.phone_number, phone_v.category, b.id \
        FROM invoice_invoice as a JOIN invoice_workorder as b on b.id = a.work_order_id \
        LEFT JOIN invoice_workitem as c on c.work_order_id = b.id \
        JOIN custom_users_vendor as v on v.id = b.vendor_id \
        JOIN custom_users_customer as d on d.id = a.customer_id \
        LEFT JOIN custom_users_contact as lut_c on d.customer_contact_id = lut_c.id \
        LEFT JOIN custom_users_contact_address as m2m_addr on lut_c.id = m2m_addr.contact_id \
        LEFT JOIN custom_users_address as addr on addr.id = m2m_addr.address_id \
        LEFT JOIN custom_users_contact_email as m2m_email on lut_c.id = m2m_email.contact_id \
        LEFT JOIN custom_users_email as email on email.id = m2m_email.email_id \
        LEFT JOIN custom_users_contact_phoneNumber as m2m_phone on lut_c.id = m2m_phone.contact_id \
        LEFT JOIN custom_users_phonenumber as phone on phone.id = m2m_phone.phonenumber_id \
        LEFT JOIN custom_users_usercontactinfo as e on e.id = a.issuer_id \
        \
        LEFT JOIN custom_users_contact as lut_v on b.vendor_id = lut_v.id \
        LEFT JOIN custom_users_contact_address as m2m_addr_v on lut_v.id = m2m_addr_v.contact_id \
        LEFT JOIN custom_users_address as addr_v on addr_v.id = m2m_addr_v.address_id \
        LEFT JOIN custom_users_contact_email as m2m_email_v on lut_v.id = m2m_email_v.contact_id \
        LEFT JOIN custom_users_email as email_v on email_v.id = m2m_email_v.email_id \
        LEFT JOIN custom_users_contact_phoneNumber as m2m_phone_v on lut_v.id = m2m_phone_v.contact_id \
        LEFT JOIN custom_users_phonenumber as phone_v on phone_v.id = m2m_phone_v.phonenumber_id \
        where a.uuid = %s and "

    # filter based on user perms (customer, issuer or vendor)
    with connection.cursor() as cursor:
        employee_sql = "SELECT e.vendor_id, uc.id as userContact FROM custom_users_employees as e    \
                            LEFT JOIN custom_users_contact as c on c.id = e.employee_id             \
                            LEFT JOIN custom_users_usercontactinfo as uc on uc.contact_id = c.id    \
                            LEFT JOIN auth_user as au on au.id = uc.user_id WHERE au.username=%s"
        cursor.execute(employee_sql, [user])
        row2 = cursor.fetchone()
        if len(row2) == 0:
            # this is a customer
            customer_sql = "SELECT c.id FROM custom_users_customer as c JOIN custom_users_contact as c2 on c2.id = c.customer_contact_id JOIN custom_users_usercontactinfo as uc on uc.contact_id = c2.id JOIN auth_user as au on au.id = uc.user_id WHERE au.username= %s;"
            cursor.execute(customer_sql, [user])
            row = cursor.fetchone()
            if len(row) == 0:
                raise ValueError('Current Signed in User is missing required data across multiple tables.')
            print('customer', row)
            cursor.execute(sql + 'a.customer_id = %s', [uuid, row[0]])
        else:
            print('employee', row2)

            cursor.execute(sql + '(a.issuer_id = %s OR b.vendor_id = %s)', [uuid, row2[1], row2[0]])
            row = cursor.fetchone()
            if row:
                customer_name = row[4].split(' ')
                name = ''
                for x in customer_name:
                    name += x.capitalize() + ' '

                return {
                    'invoice_title': row[0], 'invoice_descript': row[1], 'deadline': row[2], 'status': row[3], 
                    'customer_name': name,
                    'customer_address': f"{row[5]}  {row[6]}, {row[7]}  {row[8]}",
                    'customer_email': row[10],
                    'customer_phone': row[12],
                    'vendor_name': row[14],
                    'vendor_address': f"{row[15]}  {row[16]}, {row[17]}  {row[18]}",
                    'vendor_email' : row[20],
                    'vendor_phone': row[22],
                    'work_order': row[24]
                }
            return None

def has_permission_view_invoice(user: str, uuid: str):
    with connection.cursor() as cursor:
        sql = "Select a.id, b.order_title from invoice_invoice as a LEFT JOIN invoice_workorder as b on b.id = a.work_order_id where a.uuid = %s and "
        c = Contact.objects.get(user_contact = UserContactInfo.objects.get(user__username=user))
        if not c: 
            raise ValueError('Expected exisiting entry in Contact table for user: ', user)
        
        if Employees.objects.filter(employee=c).exists():
            sql += "a.issuer_id = %s;"
            
        else:
            sql += 'b.customer_id = %s'
            c = Customer.objects.get(customer_contact = c)
            if not c:
                raise ValueError('Expected existing entry in Customer table for user: ', user)
        c = c.pk
        cursor.execute(sql, [uuid, c])  
        return cursor.fetchone()


def get_work_items(workOrderID):
    print(workOrderID)
    with connection.cursor() as cursor:
        cursor.execute('SELECT cost, memo, descript FROM invoice_workitem JOIN invoice_workorder on invoice_workitem.work_order_id = invoice_workorder.id WHERE invoice_workorder.id = %s', [workOrderID])
        rows = cursor.fetchall()
        print(rows)
        return [{'cost': row[0], 'memo': row[1], 'descript': row[2]} for row in rows]

alphaset = set(alphabeat)
@login_required
@require_http_methods(['GET'])
@permission_required(['invoice.view_invoice'], raise_exception=True)
def viewSingleInvoice(request):
    partial_template, template_name = 'invoice/singleInvoiceView.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template

    invoice_uuid = request.GET.get('uuid')
    if not invoice_uuid:
     return render(request, template_name, {'partial_template_name': partial_template})
    for x in invoice_uuid:
        if x not in alphaset:
            print('failed validation for query param: id', x)
            return render(request, template_name, {'partial_template_name': partial_template})

    # row = has_permission_view_invoice(request.user, invoice_uuid)
    # if not row: 
    #     raise PermissionError('Unregistered User')
 
    items = None
    row = get_invoice(str(request.user), invoice_uuid)
    if row is not None:
        items = get_work_items(row['work_order'])
    return render(request, template_name, {'partial_template_name': partial_template, 'invoice': row, 'items': items})



class ViewInvoice(generic.ListView):
    # paginate_by = 25
    context_object_name = 'invoice_list'
    partial_template_name, template_name = 'invoice/view.html', 'invoicer/base.html'
    count = 0 

    def get_queryset(self):
        rows = []    
        try:
            vendor = get_vendor_by_employee(self.request.user)
        except Vendor.DoesNotExist: 
            return rows
        sql = "Select a.id, wo.id as work_item_id, a.invoice_title, a.status, a.deadline, COALESCE(SUM(wi.cost), '0.00'), a.uuid from invoice_invoice as a \
                JOIN invoice_workorder as wo ON wo.id=a.work_order_id \
                LEFT JOIN invoice_workitem as wi ON wi.work_order_id = wo.id \
                WHERE wo.vendor_id = %s \
                GROUP BY a.id, wo.id;"

        with connection.cursor() as cursor:
            cursor.execute(
                sql
                ,[vendor.pk]
                )
            rows = cursor.fetchall()
            rows = [{'uuid': row[6], 'order_title': row[2], 'status': row[3], 'deadline': row[4], 'total':row[5]} for row in rows]
        self.count = len(rows)
        return rows

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.htmx:
            self.template_name = self.partial_template_name
        
        context["count"] = self.count
        context['partial_template_name'] = self.partial_template_name
        return context
    


@login_required
def index(request):
    partial_template, template_name = 'invoice/index.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
        
    return render(request, template_name, {'partial_template_name': partial_template})

@login_required
def preview(request):
    return render(request, 'invoice/invoice_form.html', {})


'''
    INITAL: have auth_user.username
    Invoice title , status (paided), due_date , total cost
    
    Select a.id, wo.id as work_item_id, a.invoice_title, wo.status, a.deadline, COALESCE(b1.cost, '0.00') from invoice_invoice as a 
    JOIN invoice_workorder as wo ON wo.id=a.work_order_id 
    JOIN (
        Select b.work_order_id, SUM(b.cost) as cost from invoice_workitem as b GROUP BY b.work_order_id
    ) as b1 on b1.work_order_id = wo.id where wo.vendor_id=1;


    "Select a.id, wo.id as work_item_id, a.invoice_title, a.status, a.deadline, COALESCE(SUM(wi.cost), '0.00') from invoice_invoice as a /
        JOIN invoice_workorder as wo ON wo.id=a.work_order_id /
        LEFT JOIN invoice_workitem as wi ON wi.work_order_id = wo.id /
        WHERE wo.vendor_id = %s /
        GROUP BY a.id, wo.id /
        ;"
'''

