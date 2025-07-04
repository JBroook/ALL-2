from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm, UserForm, UserEditForm
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Login successful!")
        
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.add_message(self.request, messages.ERROR, "Login failed!")
        return response
    
    def get_success_url(self):
        employee = Employee.objects.get(user=self.request.user)

        if employee.virgin_login:
            print("Virgin account")
            return reverse_lazy('password_change')
            
        
        return reverse_lazy('home')
    

@role_required(['manager'])
def user_list_view(request):
    employees = Employee.objects.all()
    roles = Employee.objects.values_list('role', flat=True)
    page = "nav-users"

    return render(
        request, 
        'users/user_list.html',
        context={
            'employees' : employees,
            'roles' : roles,
            'page':page
        }
        )

def user_list_partial_view(request):
    selected_role = request.GET.get('role')
    selected_role = None if selected_role=='any' else selected_role
    employees = Employee.objects.all()
    page = "nav-users"

    if selected_role:
       employees = Employee.objects.filter(role=selected_role)

    return render(
        request,
        'partials/user_list_partial.html',
        context={
            'employees':employees,
            'search_input' : request.GET.get('role'),
            'search_criteria': 'role',
            'page':page
            })

def user_list_search_view(request):
    search_input = request.GET.get('input').strip().split()
    page = "nav-users"

    if len(search_input)==2:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=search_input[0], user__last_name__icontains=search_input[1])
        )
    else:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=request.GET.get('input')) |
            Q(user__last_name__icontains=request.GET.get('input'))
        )


    return render(
        request,
        'partials/user_list_partial.html',
        context={
            'employees':employees,
            'search_input': request.GET.get('input'),
            'search_criteria': 'name',
            'page':page
            })


def user_create_form_view(request):
    employee_form = EmployeeForm()
    user_form = UserForm()
    page = "nav-users"

    return render(
        request,
        'partials/user_create.html',
        context={
            'employee_form':employee_form,
            'user_form':user_form,
            'page': page
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
            messages.add_message(request, messages.SUCCESS, "User added!")
        else:
            messages.add_message(request, messages.ERROR, "Failed!")
        
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

                messages.add_message(request, messages.SUCCESS, "User updated!")
        
    return redirect('user_list')

def user_edit_form_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    employee_form = EmployeeForm(instance=employee)
    user_form = UserEditForm(instance=employee.user)
    page = "nav-users"

    return render(
        request,
        'partials/user_edit.html',
        context={
            'employee_form':employee_form,
            'user_form':user_form,
            'employee_id' : employee.id,
            'page': page
            }
        )

def user_info_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    page = "nav-users"

    return render(
        request,
        'partials/user_info.html',
        context={
            'employee' : employee,
            'page': page
        }
    )

def user_delete_view(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    user = employee.user
    page = "nav-users"

    if request.method=="POST":
        action_type = request.POST.get('action')

        if action_type=="confirm":
            user.delete()
            messages.add_message(request, messages.SUCCESS, "User deleted!")

        return redirect('user_list')
    else:
        return render(
            request,
            'partials/user_delete.html',
            context={
                'employee':employee,
                'page': page
            }
        )

@login_required(login_url='/users/user_login')
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

    return redirect("user_login")

class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    html_email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Email sent!")
        return response
    
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'users/change_password.html'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Password changed!")
        employee = Employee.objects.get(user=self.request.user)
        employee.virgin_login = False
        employee.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Invalid password!")
        return super().form_invalid(form)
    
    