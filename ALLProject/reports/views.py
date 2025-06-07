from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from django.db.models import F, Count, Sum
from .models import Payment, Product, CartItem, Restock, Category
from datetime import datetime,date

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')
    print(request.POST)

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
    this_month = today.strftime("%B").lower()

    all_monthly_sales = []
    sales_per_month = []
    
    total_yearly_sales = Payment.objects.filter(timeStamp__year = today.year).count()
    # print(today)
    # print(sales_per_month)

    for i in range (1,13):
        monthly_sales = Payment.objects.filter(timeStamp__month = i).count()
        all_monthly_sales.append(monthly_sales)
        sales_on_month = Payment.objects.filter(timeStamp__month = i).aggregate(revenue = Sum('total_cost'))
        sales_per_month.append(sales_on_month['revenue'])
    
    for j in range(0,len(all_monthly_sales)):
        all_monthly_sales[j] = all_monthly_sales[j] / total_yearly_sales

    # for j in range(0,12):
    #     print("Month: ",j+1)
    #     print(all_monthly_sales[j])
    # print(sales_per_month)

    # Get Restock List
    all_restock = Restock.objects.select_related('product_id').values_list(
        'product_id__supplier','product_id__name','date','cpu','product_id__quantity','units').all().annotate(unitPrice=F('units')*F('cpu'))
    # print("ALL RESTOCK DETAILS:")
    # print(all_restock)
    # for items in all_restock:
    #     print(items[1])

    # Get Today's Transactions
    total_revenue = 0
    if 'change-monthly' in request.POST:
        month_or_day = "month"
        show_transacts = Payment.objects.filter(timeStamp__month = today.month).values()
        for i in show_transacts:
            total_revenue += float(i['total_cost'])
    else:
        month_or_day = "day"
        show_transacts = Payment.objects.filter(timeStamp__day = today.day).values()
        for i in show_transacts:
            total_revenue += float(i['total_cost'])

    print(total_revenue)
    # print(transacts_day)
    # for items in transacts_day:
    #     print(items)
    print(month_or_day)
    # print(transacts_mth)
    # for items in transacts_mth:
    #     print(items)
    
    context = {
        'month': this_month,
        'best_product' : best_product,
        'category_sale' : category_sale,
        'all_monthly_sales' : all_monthly_sales,
        'sales_per_month': sales_per_month,
        'all_restock' : all_restock,
        'transacts' : show_transacts,
        'total_revenue' : total_revenue,
        'month_or_day' : month_or_day,
        }
    return HttpResponse(template.render(context,request))