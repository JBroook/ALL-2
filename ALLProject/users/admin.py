from django.contrib import admin
from . import models

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'role')

    def user_username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    user_username.short_description = 'Username'
    user_email.short_description = 'Email'

admin.site.register(models.Employee,EmployeeAdmin)