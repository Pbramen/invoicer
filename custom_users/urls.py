from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, {}),
    path('login/', views.signIn, {}),
    path('register/', views.register, {}),
    path('success/', views.success, {}),
]