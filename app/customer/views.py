from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm
from core.models import User
from django.contrib import messages


# Create your views here.


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
    return render(request, 'customer/registerCustomer.html', context)
