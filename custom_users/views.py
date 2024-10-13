from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token, csrf_protect

from .form import RegisterForm, LoginForm, PhoneForm, AddressForm
from .models import Contact, Customer, createNewUser

from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.forms import modelformset_factory



def index(request):
    return render(request, 'custom_users/index.html')

# Create your views here.
@csrf_protect
def signIn(request):
    partial_name, template_name ='custom_users/partial/sign.html', 'invoicer/base.html'
    for header in request.headers:
        if header.startswith('Cache'):
            print(header)
    
    if request.htmx:
        template_name = 'custom_users/partial/sign.html'

    content_title = 'Login'
    link = {
        "url": '/user/register/',
        "msg": 'New?',
        "clickable_msg": 'Register a new account here!'
    }


    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        print("post form recieved");
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #TODO: change this to home page
                return redirect('/')
    else:
        form = LoginForm()
    print(template_name)
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
  
        user = RegisterForm(request.POST)
        phone = PhoneForm(request.POST)
        address = AddressForm(request.POST)

        if user.is_valid() and phone.is_valid() and address.is_valid():
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

def success(request):
    partial_template, template_name = 'custom_users/partial/success.html', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
    return render(request, template_name, {'partial_template_name': partial_template})    

def logout_view(request):
    logout(request)
    partial_template, template_name = '/user/success', 'invoicer/base.html'
    if request.htmx:
        template_name = partial_template
    return redirect(template_name, {'partial_template_name': partial_template})

