from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm, UserForm, UserEditForm
from django.db.models import Q
from django.urls import reverse
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@role_required(['manager'])
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
    search_input = request.GET.get('input').strip().split()

    if len(search_input)==2:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=search_input[0], user__last_name__icontains=search_input[1])
        )
    else:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=request.GET.get('input')) |
            Q(user__last_name__icontains=request.GET.get('input'))
        )


    return render(request,'partials/user_list_partial.html',context={'employees':employees})


def user_create_form_view(request):
    employee_form = EmployeeForm()
    user_form = UserForm()

    return render(
        request,
        'partials/user_create.html',
        context={
            'employee_form':employee_form,
            'user_form':user_form,
            }
        )

def user_create_view(request):
    employee_form = EmployeeForm()
    user_form = UserForm()

    if request.method=="POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            employee_form = EmployeeForm(request.POST)
            new_employee = employee_form.save(commit=False)
            new_employee.user = new_user
            new_employee.save()
        
    return redirect('user_list')

def user_edit_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    user = employee.user

    if request.method=="POST":
        employee_form = EmployeeForm(request.POST, instance=employee)
        user_form = UserEditForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
        
        if employee_form.is_valid():
            employee.save()
        
    return redirect('user_list')

def user_edit_form_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    employee_form = EmployeeForm(instance=employee)
    user_form = UserEditForm(instance=employee.user)

    return render(
        request,
        'partials/user_edit.html',
        context={
            'employee_form':employee_form,
            'user_form':user_form,
            'employee_id' : employee.id 
            }
        )

def user_info_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)

    return render(
        request,
        'partials/user_info.html',
        context={
            'employee' : employee,
        }
    )

def user_delete_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    user = employee.user

    if request.method=="POST":
        action_type = request.POST.get('action')

        if action_type=="confirm":
            user.delete()

        return redirect('user_list')
    else:
        return render(
            request,
            'partials/user_delete.html',
            context={
                'employee':employee
            }
        )

@login_required(login_url='/accounts/login')
def home_view(request):
    employee = Employee.objects.get(user=request.user)

    return render(
        request,
        'users/home.html',
        context={
            'options' : employee.get_role_options()
        }
    )

def logout_view(request):
    logout(request)
    
    messages.add_message(request, messages.SUCCESS, "Logout successful!")

    return redirect("login")