from django.shortcuts import render
from core.models import Vendor


def profile(request):
    vendor = Vendor.objects.get(user=request.user)
    return render(request, 'vendor/profile.html')
