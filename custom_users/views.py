from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token, csrf_protect

from .form import RegisterForm, LoginForm, PhoneForm
from .models import Contact, Customer, createNewUser

from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError



def index(request):
    return render(request, 'custom_users/index.html')

# Create your views here.
@csrf_protect
def signIn(request):
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
            print(form)
    else:
        form = LoginForm()
        print(form.errors)
    return render(request, 'invoicer/form.html', {'form': [form], 'btn_display': 'Login'})


@requires_csrf_token
@transaction.atomic
def register(request):
    sys_error = None
    if request.user and request.user.is_authenticated:
        # TODO: work on a home page...
        return redirect('/')
    if request.method == 'POST':
        user = RegisterForm(request.POST)
        phone = PhoneForm(request.POST)
        if user.is_valid() and phone.is_valid():
            try:
                with transaction.atomic():
                    createNewUser(user, phone)
            except IntegrityError as ie:
                #TODO: hanlde exception here...
                sys_error = "Unable to create new user right now. Please try again later!"
                print('exited: ', ie)
            else:
                return redirect('/user/success')

    else:
        user = RegisterForm()
        phone = PhoneForm()
        return render(request, 'invoicer/form.html', {'form': [user, phone], 'btn_display': 'Register', 'sys_error':sys_error})
    pass     

def success(request):
    return render(request, 'custom_users/success.html', {})    

def logout_view(request):
    logout(request)
    return redirect('user/success')