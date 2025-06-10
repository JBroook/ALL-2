from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from django.conf import settings
from django.db.models import F, Count, Sum
from .models import Payment, Product, CartItem, Restock, Category
from .forms import printSales
from datetime import datetime,date

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from django.contrib.staticfiles import finders
from django.contrib import messages
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from io import BytesIO
import os

# Create your views here.
def ManagerReportView(request):
    template = loader.get_template('reports/partials/sales_transactions.html')
    sales_report = printSales()

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

    if 'sales_report' in request.POST:
        print("Printing Report")
        print_pdf(request)
        return HttpResponseRedirect(reverse('report'))
    
    context = {
        'sales_report': sales_report,
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
    
def add_header_footer(canvas, doc):
    # Get the page width and height
    width, height = A4
    
    title = "Sales Report"
    report_type = "Daily"
    period = "May 1 2025 - June 1 2025"
    user = "Manager Name - 2025-06-01"

    #Header
    canvas.setFont("TimesNewRoman-Bold", 20)
    canvas.drawString(232, height-25-0.5*cm, title)

    # Report Details    
    canvas.setFont("TimesNewRoman", 13)
    canvas.drawString(1.5*cm, height-65, f"Report Type -- {report_type}")
    canvas.drawString(1.5*cm, height-80, f"Date Period: {period}")
    canvas.drawString(1.5*cm, height-95, f"Generated by: {user}")
    
    # Add Logo
    logo = finders.find('images/logo.png')
    if logo:
        image_width = 2.6*cm
        image_height = 1.6*cm
        x_image = width - image_width - 50  
        y_position = height - image_height - 50

        canvas.drawImage(logo, x_image, y_position, width=image_width, height=image_height,mask="auto")

    else:
        messages.error("Logo not found. Please check if the path is correct.")
        print("Logo not found. Please check if the path is correct.")

    # Footer
    footer_text = "--- Created Using WareHub ---"
    
    # Set font and size for footer
    canvas.setFont("TimesNewRoman", 8)
    
    # Draw footer at the bottom (with margin)
    canvas.drawString(232, 0.5*cm, footer_text)

def generate_report(request):    
    title = "Sales Report"
    # check for times new romans font
    font_path = finders.find('fonts/Times New Roman.ttf')
    font_path2 = finders.find('fonts/Times New Roman - Bold.ttf')
    if font_path:
        print(f"Registering font from: {font_path}")
        pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))
        pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', font_path2))
    else:
        print("Font file 'times.ttf' not found. Falling back to 'Helvetica'.")

    # Create a buffer for the PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=4*cm, bottomMargin=4*cm)
    width, height = A4
    available_width = width-(1.5*cm*2)
    
    # Holds flowable objects
    flowables = []

    # Header
    styles = getSampleStyleSheet()

    # Main Content Table
    report_data = [
        ['Metric','Value'],
        ['Total Sales Revenue', 'RM2100.20'],
        ['Total Transactions', '50'],
        ['Average Sale Per Order', 'RM 200.18'],
        ['Total Products Sold', '311']
    ]
    report_table = Table(report_data, colWidths=[available_width*0.5, available_width*0.5])
    report_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'TimesNewRoman'),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('BOTTOMPADDING',(0,0),(-1,0),0.5*cm),
        ('GRID',(0,0),(-1,0),0.01*cm,colors.black),
    ]))
    subheader_style = styles['Heading3']
    subheader_style.fontSize = 13
    subheader_style.alignment = 1
    flowables.append(Paragraph("<b>Sales Summary</b>",subheader_style))
    flowables.append(report_table)

    # Top Products Sold Table
    products_data = [
        ['Category','Product','Sold','Revenue'],
        ['Drinks','Milk','30','RM 300.00'],
        ['Meat','Chicken','26','RM 300.00'],
        ['Electronics','Headphones','5','RM 57.50']
    ]
    products_table = Table(products_data, colWidths=[available_width*0.25, available_width*0.25, available_width*0.25, available_width*0.25])
    products_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'TimesNewRoman'),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('BOTTOMPADDING',(0,0),(-1,0),0.5*cm),
        ('GRID',(0,0),(-1,0),0.01*cm,colors.black),
    ]))
    flowables.append(Paragraph("<b>Top Products Sold</b>",subheader_style))
    flowables.append(products_table)

    # Footer
    doc.build(flowables, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    # Return PDF as a response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type ='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'

    return response
    
def print_pdf(request):
    response = generate_report(request)
    if os.name == 'nt':  # For Windows
        buffer = response.content
        with open("temp.pdf", "wb") as f:
            f.write(buffer)
        os.startfile("temp.pdf", "print")
    return response