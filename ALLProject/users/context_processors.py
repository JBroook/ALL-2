from .models import Employee

def user_role(request):
    if request.user.is_authenticated:
        try:
            if request.user.is_staff:
                pass
            else:
                return {'user_role': Employee.objects.get(user=request.user).role}
        except AttributeError:
            print("User Role: None, attribute error")
            return {'user_role': None}
    print("User Role: None")
    return {'user_role': None}