from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, {}),
    path('login/', views.signIn, {}),
    path('logout/', views.logout_view, {}),
    path('register/', views.register, {}),
    path('success/', views.success, {}),
]