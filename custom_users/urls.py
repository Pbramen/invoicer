from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, {}),
    path('login/', views.signIn, name='customer_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='customerRegister'),
    path('register/vendor/', views.vendorRegister, {}),
    path('success/', views.success, {}),
]