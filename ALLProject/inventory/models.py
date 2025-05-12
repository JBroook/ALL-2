from django.db import models

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

    def __str__(self):
        return self.name