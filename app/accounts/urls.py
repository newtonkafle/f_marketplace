from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.account_redirect),
    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('accountRedirect/', views.account_redirect, name='accountRedirect'),

    path('custDashboard/', views.custDashboard, name='customerDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),


]
