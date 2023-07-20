from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.forms import RegisterForm, RegisterVendorForm
from core.models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


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
    """ This decorator kicks irrespective user out of the view """
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

            # send verification email
            send_verification_email(request,
                                    user,
                                    'AA')

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

            # send veification email to verify the account
            send_verification_email(request, user, 'AA')
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


def activate(request, uidb64, token):
    """ activate the user by setting is_active status to true. """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        messages.error(request, 'Activation failed, Activation link invalid !')
    else:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activation successful.')
        else:
            messages.error(
                request, 'Activation failed, Activation link expired!')

    finally:
        return redirect('accountRedirect')


@login_excluded()
def login(request):
    """ login view for all the user """
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
    """ this view will redirect user to their respective view"""
    user = request.user
    if user.id is not None:
        if user.role == 1:
            return redirect('vendorDashboard')
        elif user.role == 2:
            return redirect('customerDashboard')
        elif user.role == None and user.is_superadmin:
            return redirect('/admin')
    return redirect('login')


@login_required
def logout(request):
    """ view to log out the user"""
    auth.logout(request)
    messages.info(request, 'You are successfully logged out!')
    return redirect('login')


@login_required
@permission_check('customer')
def custDashboard(request):
    """ cumstomer dashboard view"""
    return render(request, 'accounts/custDashboard.html')


@login_required
@permission_check('vendor')
def vendorDashboard(request):
    """ vendor dashboard view """
    return render(request, 'accounts/vendorDashboard.html')


def forgot_password(request):
    """ view for handling the forgot password"""
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            send_verification_email(request,
                                    user,
                                    'RP')

            messages.success(
                request, 'Password reset link sent to your email!')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exists!')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    """ view to validate the request to reset the password"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(
            request, 'Link Error, Password reset link has been modified!')
        return redirect('accountRedirect')
    else:
        if default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('reset_password')
        else:
            messages.error(
                request, 'Password reset failed, The link has been expired!')
            return redirect('accountRedirect')


def reset_password(request):
    """ view to reset the password"""
    # bugs check and error handling required

    if request.method == 'POST':
        password = request.POST['password']
        conf_password = request.POST['confirm_password']

        if password == conf_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error("Password doesn't match")
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')
