from django.shortcuts import render, get_object_or_404, redirect
from core.models import Vendor, UserProfile
from core.forms import RegisterVendorForm, UserProfileForm
from django.contrib import messages
from core.permission_manager import permission_check
from django.contrib.auth.decorators import login_required


@login_required
@permission_check('vendor')
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        vendor_form = RegisterVendorForm(
            request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated Successfully.")

            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = RegisterVendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile
    }
    return render(request, 'vendor/profile.html', context)
