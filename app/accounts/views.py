from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.forms import RegisterForm, RegisterVendorForm
from core.models import User, UserProfile
from django.contrib import messages


def registerCustomer(request):
    """view to register the customer to the database"""

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password']

            )
            user.role = User.CUSTOMER
            user.save()
            messages.success(
                request, 'Your account has been created successfully!')
            return redirect('registerCustomer')
        else:
            print(form.errors)

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerCustomer.html', context)


def registerVendor(request):
    """ view for registering the vendor """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        v_form = RegisterVendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            print(request.POST)
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password']
            )
            user.role = User.VENDOR
            user.save()

            # creating the vendor
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.success(
                request, 'Your account has been registered successfully ! Please wait for the approval')

            return redirect('registerVendor')

        else:
            print(form.errors)
            print(v_form.errors)

    else:
        form = RegisterForm()
        v_form = RegisterVendorForm()

    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return


def dashboard(request):
    return
