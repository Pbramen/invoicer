from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('create/2/', views.create2),
    path('view/', views.preview)
]
