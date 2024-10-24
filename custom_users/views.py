from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token, csrf_protect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri

from .form import RegisterForm, LoginForm, RegisterVendor, PhoneForm, AddressForm, phoneFormset, addressFormset, emailFormset, EmailForm
from .models import createCompany, createNewUser
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from django.forms import modelformset_factory
from invoicer.allowed_url import REDIRECT_ALLOWED_LIST



def index(request):
    return render(request, 'custom_users/index.html')

@csrf_protect
def vendorSignIn(request):
    partial_name, template_name = 'custom_users/partial/sign.html', 'invoicer/base.html'

    # link = {
    #     'url': '/user/register/vendor',
    #     'msg': 'New?', 
    #     'clickable_msg': 'Register a new vendor account here!'
    # }

    # return render(request, template_name, {
    #     'link': link,
    #     'partial_name': partial_name
    # })
    pass


# Create your views here.
@csrf_protect
def signIn(request):
    partial_name, template_name ='custom_users/partial/sign.html', 'invoicer/base.html'

    if request.htmx:
        template_name = 'custom_users/partial/sign.html'

    link = {
        "url": '/user/register/',
        "msg": 'New?',
        "clickable_msg": 'Register a new account here!'
    }

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
   
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                next = request.GET.get('next') 
                return redirect('/') if next is None or not url_has_allowed_host_and_scheme(iri_to_uri(next), allowed_hosts=REDIRECT_ALLOWED_LIST) else redirect(next)
        else:
            print(form.errors)
            print(form.non_field_errors)

    else:
        
        form = LoginForm()
    return render(
        request,
        template_name,
        {
            'form': [form],
            'btn_display': 'Login',
            'content_title': 'Login',
            'link': link,
            'partial_template_name': partial_name
        })


@requires_csrf_token
@transaction.atomic
def register(request):
    partial_template, template_name = 'custom_users/partial/register.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template

    sys_error = None
    content_title = 'Registration'
    link = {
        "url": '/user/login/',
        "msg": 'Already have an account?',
        "clickable_msg": 'Sign in here!'
    }
    if request.user and request.user.is_authenticated:
        # TODO: work on a home page...
        return redirect('/')
    if request.method == 'POST':
        user = RegisterForm(request.POST)
        phone = PhoneForm(request.POST)
        address = AddressForm(request.POST)
    
        if  user.is_valid() and \
            phone.is_valid() and \
            address.is_valid():

            try:
                with transaction.atomic():
                    createNewUser(user, phone, address)
            except IntegrityError as ie:
                #TODO: hanlde exception here...
                sys_error = "Unable to create new user right now. Please try again later!"
                print('exited: ', ie)

            else:
                return redirect('/user/success/')

    else:
        user = RegisterForm()
        phone = PhoneForm()
        address = AddressForm()

    return render(
        request, 
        template_name,
            {
            'form': [user, phone, address],
            'btn_display': 'Register',
            'sys_error':sys_error,
            'content_title': content_title,
            'link': link,
            'partial_template_name': partial_template
        }
    )     

@transaction.atomic
@csrf_protect
def vendorRegister(request):
    partial_template, template_name = 'custom_users/partial/register_vendor.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
    
    content_title = 'Vendor Registration'
    link = {
        "url": '/user/login/',
        "msg": 'Already have an account?',
        "clickable_msg": 'Sign in here!'
    }

    if request.method == 'POST':
        user = RegisterForm(request.POST)
        phone = PhoneForm(request.POST, prefix='user_phone' )
        address = AddressForm(request.POST, prefix='user_address')

        vendor = RegisterVendor(request.POST)
        vendor_address = AddressForm(request.POST, prefix='vendor_address')
        vendor_phone = PhoneForm(request.POST, prefix='vendor_phone')
        vendor_email = EmailForm(request.POST, prefix='vendor_email')


        if  user.is_valid() and \
            phone.is_valid() and \
            address.is_valid() and \
            vendor.is_valid() and \
            vendor_address.is_valid() and \
            vendor_phone.is_valid() and \
            vendor_email.is_valid():

            if user.is_valid() and phone.is_valid() and address.is_valid():
                try:
                    with transaction.atomic():                        
                        dict_user = createNewUser(user, phone, address)
                        print((dict_user['user']))
                        dict_user['user'].groups.add(Group.objects.get(name='vendor'))
                        createCompany(dict_user['contact'], vendor, vendor_phone, vendor_address, vendor_email)
                except IntegrityError as ie:
                    #TODO: hanlde exception here...
                    print('exited: ', ie)
                else:
                    return redirect('/user/success/')

        else: 
            print('form is invalid:')
            print(
                'user:', user.errors,
                'phone:', phone.errors,
                'address:', address.errors,
                'vendor:', vendor.errors,
                'vendor address:', vendor_address.errors,
                'vendor phone:', vendor_phone.errors,
                'vendor email:', vendor_email.errors)
        pass
    else:
        user = RegisterForm()
        address = AddressForm(prefix='vendor_address')
        phone = PhoneForm(prefix='vendor_phone')
        
        vendor = RegisterVendor()
        vendor_address = AddressForm(prefix='vendor_address')
        vendor_phone = PhoneForm(prefix='vendor_phone')
        vendor_email = EmailForm(prefix='vendor_email')

    return render(request, template_name, {        
        'user_form': user,
        'user_phone': phone,
        'user_address': address,
        'vendor_form': [vendor, vendor_address, vendor_phone, vendor_email],
        'btn_display': 'Register',
        'content_title': content_title,
        'link': link,
        'partial_template_name': partial_template
        
    })


def success(request):
    partial_template, template_name = 'custom_users/partial/success.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
    return render(request, template_name, {'partial_template_name': partial_template})    
  

def logout_view(request):
    logout(request)
    return redirect('/user/success')