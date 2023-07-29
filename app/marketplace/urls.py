from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>', views.vendorDetail, name='vendor_detail'),

    # cart functionality
    path('add_to_cart/<int:product_id>/', views.addToCart, name='add_to_cart'),
    path('decrease_cart/<int:product_id>/',
         views.decreaseCart, name='decrease_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart/<int:cart_id>/', views.deleteCart, name='delete_cart')

]
