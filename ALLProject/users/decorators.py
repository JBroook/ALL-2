from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import Employee
from django.contrib import messages
from django.http import HttpResponseBadRequest

def ajax_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method=="POST":
            has_pass = request.POST.get('has_pass')
        else:
            has_pass = request.GET.get('has_pass')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or has_pass:
            return view_func(request, *args, **kwargs)
        return HttpResponseBadRequest("AJAX requests only.")
    return _wrapped_view


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, "Not logged in!")
                return redirect("user_login")
            
            employee = Employee.objects.get(user=request.user)

            if employee.role in allowed_roles:
                if not employee.virgin_login:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR, "Password not changed yet!")
                    return redirect("password_change")
            else:
                messages.add_message(request, messages.ERROR, "Required role missing!")
                return HttpResponseForbidden("You do not have permission to access this page.")
        
        return _wrapped_view
    return decorator
