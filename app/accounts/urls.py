from django.urls import path
from . import views


urlpatterns = [
    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
