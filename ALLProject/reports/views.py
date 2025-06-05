from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from django.db.models import F
from .models import Payment, Product, CartItem, Restock
from datetime import date

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')

    # Get Best Selling Products
    all_products = Product.objects.all().values()
    all_cart_items = CartItem.objects.all().values()
    total_sold=0
    best_product = []

    for item in all_products:
        for sold in all_cart_items:
            if sold['product_id'] == item['id']:
                total_sold += sold['quantity']
        best_product.append({'product': item['name'], 'quantity_sold' : total_sold, 'image': f"{settings.MEDIA_URL}{item['image']}" if item['image'] else ''})
        total_sold = 0
    best_product.sort(key=lambda x:x['quantity_sold'])
    best_product.reverse()
    #print(best_product)

    # Get Restock List
    all_restock = Restock.objects.select_related('product_id').values_list(
        'product_id__supplier','product_id__name','date','cpu','product_id__quantity','units').all().annotate(unitPrice=F('units')*F('cpu'))
    print("ALL RESTOCK DETAILS:")
    print(all_restock)
    for items in all_restock:
        print(items[1])

    # Get Today's Transactions
    today = date.today()
    #print(today)
    transacts = Payment.objects.filter(timeStamp__contains = '2025-06-04')
    
    context = {
        'best_product' : best_product,
        'all_restock' : all_restock,
        'transacts' : transacts,
        }
    return HttpResponse(template.render(context,request))