from django import forms
from .models import Employee
# from django.contrib.auth.models import User

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','email','password']
#         labels = {
#             'username' : "Username",
#             'email' : "Email",
#             'password' : 'Password',
#         }

#         widgets = {
#             'username' : forms.TextInput(
#                 attrs={
#                     'placeholder':'e.g. JohnAdam', 'class':'form-control'
#                     }),
#             'email' : forms.TextInput(
#                 attrs={
#                     'placeholder':'e.g. johnadam@gmail.com', 'class':'form-control'
#                     }),
#             'password' : forms.PasswordInput(
#                 attrs={
#                     'placeholder':'*******', 'class':'form-control'
#                     }),
#         }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['role']
        labels = {
            'role' : "Role",
        }

        widgets = {
            'role' : forms.Select(
                attrs={
                    'class':'form-control'
                    }),
        }