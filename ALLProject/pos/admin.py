from django.contrib import admin
from . import models

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_ID', 'total_cost')

    def cart_ID(self, obj):
        return obj.id
    
    def total_cost(self,obj):
        return obj.total_cost

    cart_ID.short_description = 'Cart ID'
    total_cost.short_description = 'Amount Paid'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_ID', 'product_name', 'quantity','total_cost')

    def cart_ID(self, obj):
        return obj.cart

    def product_name(self, obj):
        return obj.product.name
    
    def quantity(self,obj):
        return obj.quantity
    
    def total_cost(self,obj):
        return obj.total_cost
    
    cart_ID.short_description = 'Cart ID'
    product_name.short_description = 'Product'
    quantity.short_description = 'Quantity'
    total_cost.short_description = 'Total Cost'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_method','cart','total_cost')

    def cart(self,obj):
        return obj.cart_id

    def payment_method(self,obj):
        return obj.payment_method
    
    def total_cost(self,obj):
        return obj.total_cost

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Payment, PaymentAdmin)