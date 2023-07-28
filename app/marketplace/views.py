from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import Vendor, Category, Product, Cart
from django.db.models import Prefetch


def marketplace(request):
    """ view for the marketplace. """
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    counter = vendors.count()
    context = {
        'vendors': vendors,
        'counter': counter
    }
    return render(request, 'marketplace/market_home.html', context)


def vendorDetail(request, vendor_slug=None):
    """ view for showing all the food items of vendor"""
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(is_available=True)
        )
    )

    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def addToCart(request, product_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id=product_id)
                try:
                    checkCart = Cart.objects.get(
                        user=request.user, product=product)
                    checkCart.quantity += 1
                    checkCart.save()
                except:
                    checkCart = Cart.objects.create(
                        user=request.user, product=product, quantity=1)
            except:
                return JsonResponse({'status': 'Failed', 'message': 'product does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request!'})
    return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})
