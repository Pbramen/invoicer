from django.shortcuts import render, redirect
from .models import Invoice
from django.forms import modelformset_factory

# Create your views here.
def index(request):

    return redirect('/user', {})