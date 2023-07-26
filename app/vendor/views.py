from django.shortcuts import render, get_object_or_404, redirect
from core.models import Vendor, UserProfile, Category, Product
from core.forms import RegisterVendorForm, UserProfileForm, CategoryForm
from django.contrib import messages
from core.permission_manager import permission_check
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify


def get_vendor(request):
    """ helper function to get vendor"""
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required
@permission_check('vendor')
def profile(request):
    """ view to show the vendor profile. """
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


# _________vendor_menu___________#
@login_required
@permission_check('vendor')
def menu_builder(request):
    """ view for handling the menus items. """
    categories = Category.objects.filter(
        vendor=get_vendor(request)).order_by('created_at')
    context = {
        'categories': categories,
        'range': categories.count()
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required
@permission_check('vendor')
def productsByCategory(request, pk=None):
    """ view for showing products and their category"""
    category = get_object_or_404(Category, pk=pk)
    product = Product.objects.filter(
        vendor=get_vendor(request), category=category)
    context = {
        'products': product,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


def addCategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category_name = form.cleaned_data['category_name']
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()

    context = {
        'form': form
    }

    return render(request, 'vendor/add_category.html', context)


def editCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(form.cleaned_data['category_name'])
            form.save()
            messages.success(request, 'Category updatede successfully!')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }

    return render(request, 'vendor/edit_category.html', context)


def deleteCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category Deleted!')
    return redirect('menu_builder')
