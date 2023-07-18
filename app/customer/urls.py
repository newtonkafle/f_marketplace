from django.urls import path
from . import views


urlpatterns = [
    path('registerCustomer/', views.registerCustomer, name='registerCustomer')
]
