from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.forms import RegisterForm, RegisterVendorForm
from core.models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


def login_excluded():
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                messages.warning(request, 'You are already logged in!')
                return redirect('accountRedirect')
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


def permission_check(view_name):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            role = f'{request.user.get_role_display().lower()}'
            if role != view_name:
                messages.warning(request, 'Permission Denied!')
                return redirect('accountRedirect')
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


@login_excluded()
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


@login_excluded()
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


@login_excluded()
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('accountRedirect')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def account_redirect(request):
    user = request.user
    if user.role == 1:
        return redirect('vendorDashboard')
    elif user.role == 2:
        return redirect('customerDashboard')
    elif user.role is None and user.is_superadmin:
        return redirect('/admin')
    return redirect('login')


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are successfully logged out!')
    return redirect('login')


@login_required
@permission_check('customer')
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required
@permission_check('vendor')
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
