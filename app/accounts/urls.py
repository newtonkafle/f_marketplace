from django.urls import path
from . import views


urlpatterns = [
    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('accountRedirect/', views.account_redirect, name='accountRedirect'),
    path('custDashboard/', views.custDashboard, name='customerDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]
