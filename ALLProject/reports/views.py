from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from .models import Payment, Product, CartItem
from datetime import date

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')

    # Get Best Selling Products
    all_products = Product.objects.all().values()
    all_cart_items = CartItem.objects.all().values()
    total_sold=0
    # print("Fetched Products: ")
    # for names in all_products:
    #     print(names)
    # print("Fetched Cart Items: ")
    # for names in all_cart_items:
    #     print(names)
    best_product = []
    for item in all_products:
        # print("product id: ",item['id'])
        for sold in all_cart_items:
            if sold['product_id'] == item['id']:
                total_sold += sold['quantity']
        best_product.append({'product': item['name'], 'quantity_sold' : total_sold, 'image': f"{settings.MEDIA_URL}{item['image']}" if item['image'] else ''})
        total_sold = 0
    best_product.sort(key=lambda x:x['quantity_sold'])
    best_product.reverse()
    #print(best_product)
    # for items in best_product:
    #     print(items['product'])

    # Get Today's Transactions
    today = date.today()
    #print(today)
    transacts = Payment.objects.filter(timeStamp__contains = today)
    
    context = {
        'best_product' : best_product,
        'transacts' : transacts,
        }
    return HttpResponse(template.render(context,request))