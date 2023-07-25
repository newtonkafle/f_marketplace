""" handling the context processors"""
from .models import Vendor
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
