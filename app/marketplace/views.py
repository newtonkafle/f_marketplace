from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from core.models import Vendor, Category, Product, Cart
from django.db.models import Prefetch
from core.context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required


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
    cart_items = None
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
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
                    return JsonResponse({'status': 'success',
                                         'message': 'Cart quantity increased',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': checkCart.quantity,
                                         'amounts': get_cart_amounts(request),
                                         })
                except:
                    checkCart = Cart.objects.create(
                        user=request.user, product=product, quantity=1)
                    return JsonResponse({'status': 'success',
                                         'message': 'new cart created',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': checkCart.quantity,
                                         'amounts': get_cart_amounts(request),
                                         })
            except:
                return JsonResponse({'status': 'failed',
                                     'message': 'product does not exist'})
        else:
            return JsonResponse({'status': 'failed',
                                 'message': 'Invalid Request!'})
    return JsonResponse({'status': 'login-required',
                         'message': 'Please login to continue'})


def decreaseCart(request, product_id=None):

    if request.user.is_authenticated:
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'failed', 'message': 'Invalid Request!'})
        else:
            try:
                product = Product.objects.get(id=product_id)
            except:
                return JsonResponse({'status': 'failed',
                                     'message': 'product does not exist'})
            else:
                try:
                    checkCart = Cart.objects.get(
                        user=request.user, product=product)
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.quantity = 0
                        checkCart.delete()
                    return JsonResponse({'status': 'success',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': checkCart.quantity,
                                         'amounts': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'failed',
                                         'message': 'Item does not exists on cart'})

    return JsonResponse({'status': 'login-required',
                         'message': 'Please login to continue'})


@login_required
def cart(request):
    """show the current cart items """
    cart = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart': cart,
    }
    return render(request, 'marketplace/cart.html', context)


@login_required
def deleteCart(request, cart_id=None):
    """ delete the request cart. """
    if request.user.is_authenticated:
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'failed', 'messages': 'Invalid Request!'})
        try:
            cart = Cart.objects.get(user=request.user, id=cart_id)
            if cart:
                cart.delete()
                return JsonResponse({'status': 'success',
                                     'message': 'Cart Item Deleted',
                                     'cart_counter': get_cart_counter(request),
                                     'amounts': get_cart_amounts(request)})
        except:
            return JsonResponse({'status': 'failed', 'message': 'Cart item does not exists!'})
    return JsonResponse({'status': 'login-required', 'message': 'Please login to continue'})
