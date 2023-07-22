""" contains all the permission decorator for the application"""
from django.contrib import messages
from django.shortcuts import redirect


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
