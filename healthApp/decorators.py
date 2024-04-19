from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

def admin_required(view_func):
    """
    Decorator to ensure that the user is an admin.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is authenticated and is an admin
        if request.user.is_authenticated and request.user.is_superuser:
            # User is an admin, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not an admin, return forbidden response
            return redirect('login')

    return _wrapped_view
