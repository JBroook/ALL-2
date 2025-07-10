from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pathlib import Path
from django.core.validators import MinValueValidator

import random
from io import BytesIO
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
from users.models import Employee
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
from reportlab.lib.units import mm
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    quantity = models.IntegerField(
        verbose_name='Quantity',
        validators=[MinValueValidator(0, message="Value must be zero or greater.")]
        )
    image = models.ImageField(upload_to='products/',default='/media/products/20240322_200331.jpg')
    supplier = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(validators=[MinValueValidator(0, message="Value must be zero or greater.")])
    alert_threshold = models.IntegerField(validators=[MinValueValidator(0, message="Value must be zero or greater.")])
    qr_code = models.ImageField(upload_to='qr/')
    barcode_number = models.CharField(max_length=50,unique=True,blank=True,null=True)
    barcode_img = models.ImageField(upload_to='barcode/',blank=True,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    sku = models.CharField(max_length=10, verbose_name="Stock Keeping Unit")

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
            qr_data = qrcode.make(f"Name: {self.name}\nCategory: {self.category}\nPrice: RM {self.price}\nBarcode Number: {self.barcode_number}")
            qr_image = qrcode.make(qr_data)

            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            buffer.seek(0)

            filename = f"{self.name}_qr.png"
            file_path = os.path.join('qr', filename)

            # Save the in-memory file to the model's ImageField/FileField
            self.qr_code.save(filename, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def low_stock_alert(self):
        text_content = render_to_string(
            "inventory/low_stock_alert.txt",
            context={"product": self},
        )

        html_content = render_to_string(
            "inventory/low_stock_alert_email.html",
            context={"product": self},
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

    def deduct_stock(self, stock_to_deduct):
        self.quantity -= stock_to_deduct
        print("Stock deducted")
        if self.quantity <= self.alert_threshold:
            print("Low stock alert sent")
            self.low_stock_alert()

    def print_codes(self):
        qr_code_path = Path(str(settings.BASE_DIR)+self.qr_code.url)
        barcode_path = Path(str(settings.BASE_DIR)+self.barcode_img.url)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.name}_qr_code_{self.id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(width/2, height - 50, f"QR Code for Product: {self.name}")

        p.drawImage(qr_code_path, x=width/2 - 25 * mm, y=height - 200, width=50 * mm, height=50 * mm)

        p.drawCentredString(width/2, height - 220, f"Barcode for Product: {self.name}")

        p.drawImage(barcode_path, x=width/2 - 40 * mm, y=height - 400, width=80 * mm, height=50 * mm)

        p.showPage()
        p.save()

        return response
    
    def print_code_to(self, p):
        qr_code_path = Path(str(settings.BASE_DIR)+self.qr_code.url)
        barcode_path = Path(str(settings.BASE_DIR)+self.barcode_img.url)

        width, height = A4
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(width/2, height - 50, f"QR Code for Product: {self.name}")

        p.drawImage(qr_code_path, x=width/2 - 25 * mm, y=height - 200, width=50 * mm, height=50 * mm)

        p.drawCentredString(width/2, height - 220, f"Barcode for Product: {self.name}")

        p.drawImage(barcode_path, x=width/2 - 40 * mm, y=height - 400, width=80 * mm, height=50 * mm)

        p.showPage()

    
class Restock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    date = models.DateField(verbose_name='Date', default=timezone.now)
    units = models.IntegerField(
        verbose_name='Stock Added',
        validators=[MinValueValidator(0, message="Value must be zero or greater.")]
        )
    cpu = models.FloatField(
        verbose_name='Cost Per Unit',
        validators=[MinValueValidator(0, message="Value must be zero or greater.")]
        )
    
    def get_total_cost(self):
        return self.units * self.cpu
    
    def __str__(self):
        return self.product.name
    
    def change_quantity(self):
        self.product.quantity += self.units
        self.product.save()

