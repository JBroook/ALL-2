from django.db import models
from inventory.models import Product
from users.models import Employee

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
    card_info = models.CharField(max_length=16, null=True)
    expiry = models.CharField(max_length=5,null=True)
    cvv = models.CharField(max_length=4,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
