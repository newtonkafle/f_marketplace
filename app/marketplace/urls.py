from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>', views.vendorDetail, name='vendor_detail'),

    # cart functionality
    path('add_to_cart/<int:product_id>/', views.addToCart, name='add_to_cart')

]
