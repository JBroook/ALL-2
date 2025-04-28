from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    quantity = models.IntegerField(verbose_name='Quantity')
    qr_code = models.ImageField(upload_to='products/')
    supplier = models.CharField(max_length=100),
    category = models.ForeignKey(Category, on_delete=models.CASCADE)