from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings

import random
from io import BytesIO
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    quantity = models.IntegerField(verbose_name='Quantity')
    image = models.ImageField(upload_to='products/',default='/media/products/20240322_200331.jpg')
    supplier = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    alert_threshold = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr/')
    barcode_number = models.CharField(max_length=50,unique=True,blank=True,null=True)
    barcode_img = models.ImageField(upload_to='barcode/',blank=True,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.barcode_number:
            number = ''.join(random.choices('0123456789',k=12))
            ean = EAN13(number, writer=ImageWriter())

            buffer = BytesIO()
            ean.write(buffer)
            self.barcode_img.save(f"{self.name}_barcode.png", File(buffer), save=False)
            self.barcode_number = ean.__str__()
        
        if not self.qr_code:    
            image = qrcode.make(f"Name: {self.name}\nCategory: {self.category}\nPrice: RM {self.price}\nBarcode Number: {self.barcode_number}")
            filename = f"{self.name}_{self.id}_qr.png"
            image.save(str(settings.BASE_DIR)+'/media/qr/'+ filename)

            self.qr_code = '/qr/'+ filename
            
        super().save(*args, **kwargs)
    
class Restock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date', default=timezone.now)
    units = models.IntegerField(verbose_name='Stock Added')
    cpu = models.FloatField(verbose_name='Cost Per Unit')
    
    def get_total_cost(self):
        return self.units * self.cpu
    
    def __str__(self):
        return self.product.name

