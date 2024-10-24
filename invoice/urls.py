from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('view/', views.ViewInvoice.as_view(), name='invoice_list'),
    path('viewInvoice/', views.viewSingleInvoice)
]
