""" handling the context processors"""
from .models import Vendor, Cart, Product
from django.conf import settings


def get_vendor(request):
    """ this function will load the vendor in all the context"""
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


def get_google_api(request):
    """ load google api key in all the context"""
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


# ----market-place context processors-----#
def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_items in cart_items:
                    cart_count += cart_items.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    gst = 0
    total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        for item in cart:
            subtotal += (item.product.price * item.quantity)
        total = subtotal + gst
    return dict(subtotal=subtotal, gst=gst, total=total)
