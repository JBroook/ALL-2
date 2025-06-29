from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(
        choices=[
            ('cashier', 'Cashier'),
            ('admin', 'Admin'),
            ('manager', 'Manager')
        ]
    )
    virgin_login = models.BooleanField(default=True)
    
    def get_role_options(self):
        options = [
            {
                'title' : 'Inventory',
                'roles' : ['admin', 'manager'],
                'description' : 'Add, view, edit and restock products',
                'image' : 'images/purple-shipping.png',
                'url' : reverse('product_list')
            },
            {
                'title' : 'Category',
                'roles' : ['admin', 'manager'],
                'description' : 'View and manage categories for products',
                'image' : 'images/purple-category.png',
                'url' : reverse('category')
            },
            {
                'title' : 'Sales Report',
                'roles' : ['manager'],
                'description' : 'View detailed analyses of performance and generate reports',
                'image' : 'images/purple-report.png',
                'url' : reverse('user_list')
            },
            {
                'title' : 'Users',
                'roles' : ['manager'],
                'description' : 'Manage existing users or add new employees',
                'image' : 'images/purple-users.png',
                'url' : reverse('user_list')
            },
            {
                'title' : 'Item Scanning',
                'roles' : ['cashier'],
                'description' : 'Start scanning items for customers',
                'image' : 'images/purple-barcode.png',
                'url' : reverse('sales')
            },
            {
                'title' : 'Sales History',
                'roles' : ['cashier'],
                'description' : 'View all previous sales and transactiond details',
                'image' : 'images/purple-history.png',
                'url' : reverse('history')
            }
        ]

        filtered_options = []

        for i in range(len(options)):
            if self.role in options[i]['roles']:
                filtered_options.append(options[i])

        return filtered_options
    
    def call_manager(self):
        text_content = render_to_string(
            "pos/call_manager_text.txt",
            context={"user": self.user},
        )

        html_content = render_to_string(
            "pos/call_manager_email.html",
            context={"user": self.user},
        )

        managers = Employee.objects.filter(role='manager')

        msg = EmailMultiAlternatives(
            "Manager Help Requested",
            text_content,
            None,
            [manager.user.email for manager in managers],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()