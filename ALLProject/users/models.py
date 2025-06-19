from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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


# rec_login_required = user_passes_test(lambda u: True if u.is_recruiter else False, login_url='/')

# def recruiter_login_required(view_func):
#     decorated_view_func = login_required(rec_login_required(view_func), login_url='/')
#     return decorated_view_func

# @recruiter_login_required
# def index(request):
#     return render(request, 'index.html')