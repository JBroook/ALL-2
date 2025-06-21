from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import Employee
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, "Not logged in!")
                return redirect("user_login")
            
            user_role = Employee.objects.get(user=request.user).role

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.add_message(request, messages.ERROR, "Required role missing!")
                return HttpResponseForbidden("You do not have permission to access this page.")
        
        return _wrapped_view
    return decorator
