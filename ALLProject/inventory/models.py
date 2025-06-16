from django.db import models
import datetime

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

    def __str__(self):
        return self.name
    
class Restock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date', default=datetime.datetime.now())
    units = models.IntegerField(verbose_name='Stock Added')
    cpu = models.FloatField(verbose_name='Cost Per Unit')
    
    def get_total_cost(self):
        return self.units * self.cpu
    
    def __str__(self):
        return self.product.name

