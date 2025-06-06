from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from django.db.models import F, Count, Sum
from .models import Payment, Product, CartItem, Restock, Category
from datetime import datetime

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')

    # Get Best Selling Products
    all_products = Product.objects.all().values()
    all_cart_items = CartItem.objects.all().values()
    total_product_sold=0
    best_product = []

    for item in all_products:
        for sold in all_cart_items:
            if sold['product_id'] == item['id']:
                total_product_sold += sold['quantity']
        best_product.append({'product': item['name'], 'quantity_sold' : total_product_sold, 'image': f"{settings.MEDIA_URL}{item['image']}" if item['image'] else ''})
        total_product_sold = 0
    
    best_product.sort(key=lambda x:x['quantity_sold'])
    best_product.reverse()
    #print(best_product)

    # Sales for each category (Donut Chart)
    total_sold = CartItem.objects.aggregate(total=Sum('quantity'))
    category_sale = list(Category.objects.values('name').annotate(total=Sum('product__cartitem__quantity')))
    category_sale = [item for item in category_sale if item['total'] is not None]
    for i in category_sale:
        percentage = round(((i['total']/total_sold['total']) * 360),2)
        i.update({'y':percentage})
    # print(total_sold)
    # print(category_sale)

    # Sales made for each months within the year
    today = datetime.now()
    all_monthly_sales = []
    total_yearly_sales = Payment.objects.filter(timeStamp__year = today.year).count()
    print(today.month)

    for i in range (1,13):
        monthly_sales = Payment.objects.filter(timeStamp__month = i).count()
        all_monthly_sales.append(monthly_sales)
    
    for j in range(0,len(all_monthly_sales)):
        all_monthly_sales[j] = all_monthly_sales[j] / total_yearly_sales

    for j in range(0,12):
        print("Month: ",j+1)
        print(all_monthly_sales[j])
    print(all_monthly_sales)

    # Get Restock List
    all_restock = Restock.objects.select_related('product_id').values_list(
        'product_id__supplier','product_id__name','date','cpu','product_id__quantity','units').all().annotate(unitPrice=F('units')*F('cpu'))
    # print("ALL RESTOCK DETAILS:")
    # print(all_restock)
    # for items in all_restock:
    #     print(items[1])

    # Get Today's Transactions
    #print(today)
    transacts_day = Payment.objects.filter(timeStamp__day = today.day).values()
    transacts_mth = Payment.objects.filter(timeStamp__month = today.month).values()
    # print(transacts_day)
    # for items in transacts_day:
    #     print(items)
    # print("ah")
    # print(transacts_mth)
    # for items in transacts_mth:
    #     print(items)

    this_month = today.strftime("%B").lower()
    
    context = {
        'month': this_month,
        'best_product' : best_product,
        'category_sale' : category_sale,
        'all_monthly_sales' : all_monthly_sales,
        'all_restock' : all_restock,
        'transacts' : transacts_day,
        }
    return HttpResponse(template.render(context,request))