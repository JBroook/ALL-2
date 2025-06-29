from django.db import models
import datetime
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from users.models import Employee
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    quantity = models.IntegerField(verbose_name='Quantity')
    image = models.ImageField(upload_to='products/',default='/media/products/20240322_200331.jpg')
    qr_code = models.ImageField(upload_to='qr/')
    supplier = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    alert_threshold = models.IntegerField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    sku = models.CharField(max_length=10, verbose_name="Stock Keeping Unit")

    def __str__(self):
        return self.name
    
    def low_stock_alert(self):
        text_content = render_to_string(
            "inventory/low_stock_alert.txt",
            context={"product": self},
        )

        html_content = render_to_string(
            "inventory/low_stock_alert_email.html",
            context={"produc": self},
        )

        admin_managers = Employee.objects.filter(Q(role='manager') | Q(role='admin'))

        msg = EmailMultiAlternatives(
            f"{self.name} low in stock",
            text_content,
            None,
            [person.user.email for person in admin_managers],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
class Restock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date', default=timezone.now)
    units = models.IntegerField(verbose_name='Stock Added')
    cpu = models.FloatField(verbose_name='Cost Per Unit')
    
    def get_total_cost(self):
        return self.units * self.cpu
    
    def __str__(self):
        return self.product.name

