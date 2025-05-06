from django.contrib import admin
from . import models

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','types','stock')

    def types(self, obj):
        return len(obj.product_set.all())
    
    def stock(self, obj):
        total = 0
        for product in obj.product_set.all():
            total += product.quantity

        return total


admin.site.register(models.Product)
admin.site.register(models.Category, CategoryAdmin)