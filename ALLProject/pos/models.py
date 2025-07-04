from django.http import HttpResponse
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from inventory.models import Product
from users.models import Employee

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from django.conf import settings
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer

# Create your models here.
class Cart(models.Model):
    total_cost = models.FloatField(default=0.00)
    payment_status = models.BooleanField(null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def get_cart_total(self):
        return sum(item.get_product_total() for item in self.cart_items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1,null=False)
    total_cost = models.FloatField(default=0.00)

    def get_product_total(self):
        return self.product.price * self.quantity
    
class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    employeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=12,null=False)
    tax = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    total_cost = models.FloatField(default=0.00,null=False)
    card_info = models.CharField(max_length=256, null=True)
    expiry = models.CharField(max_length=256,null=True)
    cvv = models.CharField(max_length=256,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.card_info and not self.card_info.startswith('pbkdf2_'): # Check if card_info is not already hashed
            self.card_info = make_password(self.card_info)
        if self.expiry and not self.expiry.startswith('pbkdf2_'): # Check if expiry is not already hashed
            self.expiry = make_password(self.expiry)
        if self.cvv and not self.cvv.startswith('pbkdf2_'): # Check if cvv is not already hashed
            self.cvv = make_password(self.cvv)
            
        super().save(*args, **kwargs)
            
    def print_payment(self):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.timeStamp}_receipt_{self.id}.pdf"'

        c = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        y = height - 30 * mm  # Start a bit lower

        # Header
        c.setFont("Helvetica", 10.5)
        c.drawCentredString(width / 2, y, f"Created on {self.timeStamp}.")
        y -= 12
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, y, f"Receipt Number: {self.id}")
        y -= 30

        # Product table
        data = [
            ["Item Code", "Product Name", "Unit Price"]
        ]
        for cart_item in CartItem.objects.filter(cart=self.cart):
            l = [str(cart_item.product.id), f"{cart_item.product.name} x{cart_item.quantity}", str(cart_item.product.price)]
            data.append(l)

        table = Table(data, colWidths=[50 * mm, 50 * mm, 50 * mm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, 30 * mm, y - 30)
        y -= 60

        # Line
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(30 * mm, y, width - 30 * mm, y)
        y -= 10

        # Summary section
        summary_data = [
            ["SUB-TOTAL", f"RM{self.cart.total_cost:.2f}"],
            ["Discount", f"RM{self.discount:.2f}"]
        ]
        summary_table = Table(summary_data, colWidths=[100 * mm, 50 * mm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        summary_table.wrapOn(c, width, height)
        summary_table.drawOn(c, 30 * mm, y - 45)
        y -= 65

        # Line
        c.line(30 * mm, y, width - 30 * mm, y)
        y -= 15

        # Total to pay
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(30 * mm, y, "TOTAL TO PAY")
        c.drawRightString(width - 30 * mm, y, f"RM{self.total_cost:.2f}")
        y -= 18

        # Cash method
        c.setFont("Helvetica", 10)
        c.drawString(30 * mm, y, "Cash")

        c.showPage()
        c.save()

        return response