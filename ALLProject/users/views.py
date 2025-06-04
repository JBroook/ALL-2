from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def user_list_view(request):
    employees = Employee.objects.all()
    roles = Employee.objects.values_list('role', flat=True)

    return render(
        request, 
        'users/user_list.html',
        context={
            'employees' : employees,
            'roles' : roles
        }
        )

def user_list_partial_view(request):
    selected_role = request.GET.get('role')
    selected_role = None if selected_role=='any' else selected_role
    employees = Employee.objects.all()

    if selected_role:
       employees = Employee.objects.filter(role=selected_role)

    return render(request,'partials/user_list_partial.html',context={'employees':employees})

def user_list_search_view(request):
    search_input = request.GET.get('input')

    employees = Employee.objects.filter(user__username__icontains=search_input)

    return render(request,'partials/user_list_partial.html',context={'employees':employees})


def user_create_view(request):
    employee_form = EmployeeForm()
    user_form = UserCreationForm()

    if request.method=="POST":
        print("post detected")
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            print("valid user detected")
            new_user = user_form.save()
            employee_form = EmployeeForm(request.POST)
            new_employee = employee_form.save(commit=False)
            new_employee.user = new_user
            new_employee.save()

            return redirect('user_list')

    return render(
        request,
        'partials/user_create.html',
        context={
            'employee_form':employee_form,
            'user_form':user_form,
            }
        )

