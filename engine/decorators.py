from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
                return redirect("login")

            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)

            messages.error(request, "You do not have permission to access this page.")
            return redirect("dashboard")

        return wrapper
    return decorator
