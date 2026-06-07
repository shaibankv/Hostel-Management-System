from functools import wraps
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def role_required(allowed_roles):
    """
    Decorator to restrict access to users with specific roles.
    If a user is not authenticated, they are redirected to login.
    If they are authenticated but do not have an allowed role, they are logged out,
    shown an unauthorized message, and redirected to the login page.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
        
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                logout(request)
                messages.error(request, "Unauthorized access. You have been logged out.")
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
