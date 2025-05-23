from django.contrib import admin
from . import models

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_ID', 'no_of_product', 'total_cost')

    def cart_ID(self, obj):
        return obj.id

    def no_of_product(self, obj):
        return obj.product.count()
    
    def total_cost(self,obj):
        return obj.total_cost

    cart_ID.short_description = 'Cart ID'
    no_of_product.short_description = 'Types of Products Bought'
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

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Payment)