from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Vendor, Product
from django.db.models import Q


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors': vendors,
    }
    return render(request, 'home.html', context)


def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['long']
    radius = request.GET['custom-radius']
    rest_food_name = request.GET['resturant-name']

    # filtering the resturant by resturant name and the food item name
    fetch_vendor_by_product = Product.objects.filter(
        product_title__icontains=rest_food_name, is_available=True).values_list('vendor', flat=True)
    q1 = Q(id__in=fetch_vendor_by_product)
    q2 = Q(vendor_name__icontains=rest_food_name,
           is_approved=True, user__is_active=True)

    vendors = Vendor.objects.filter(q1 | q2)

    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'counter': vendor_count,
    }
    return render(request, 'marketplace/market_home.html', context)
