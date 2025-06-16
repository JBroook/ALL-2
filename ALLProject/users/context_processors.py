from users.models import Employee

def user_role(request):
    if request.user.is_authenticated:
        role = Employee.objects.get(user=request.user).role
        return {'user_role': role}
    return {'user_role': None}