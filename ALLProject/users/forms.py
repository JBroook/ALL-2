from django import forms
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

        widgets = {
            'username' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. JohnAdam', 'class':'form-control'
                    }),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': '*******',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '*******',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'e.g. johnadam@gmail.com',
            'class': 'form-control'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'e.g. John',
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'e.g. Adams',
            'class': 'form-control'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        exclude = ['password']

        widgets = {
            'username' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. JohnAdam', 'class':'form-control'
                    }),
            'email' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. johnadam@gmail.com', 'class':'form-control'
                    }),
            'first_name' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. John', 'class':'form-control'
                    }),
            'last_name' : forms.TextInput(
                attrs={
                    'placeholder':'e.g. Adam', 'class':'form-control'
                    }),
        }

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

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(required=True)
    def clean(self):
        super(CustomAuthenticationForm, self).clean()
        email = self.cleaned_data.get('email')
        if email:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=self.cleaned_data.get('password')
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Invalid email or password'
                )
        return self.cleaned_data