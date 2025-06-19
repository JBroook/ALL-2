from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Restock
from .forms import ProductForm, RestockForm, CategoryForm
from django.conf import settings
from django.db.models import Count, Avg, Sum
from django.urls import reverse
from pathlib import Path
from users.decorators import role_required

import qrcode
import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
from reportlab.lib.units import mm

@role_required(['admin','manager'])
def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by("name")

    return render(
        request,
        'inventory/product_list.html',
        context={
            'products' : products,
            'product_count': len(products),
            'categories' : categories
        }
    )

def product_list_partial_view(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    availability = request.GET.get('availability')

    if category!='none':
        products = products.filter(category__name=category)

    if availability!='none':
        info = {
            'low':5,
            'zero':0
        }
        products = products.filter(quantity__lte=info[availability])
    
    return render(
        request,
        'partials/product_list_partial.html',
        context={
            'products' : products
        }
    )

def product_info_view(request, product_id):
    product = Product.objects.get(pk=product_id)

    return render(
        request,
        'partials/product_info.html',
        context={
            'chosen_product' : product
        }
    )

def product_create_view(request):
    form = ProductForm()

    if request.method=="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            
            image = qrcode.make("Pooop")
            filename = f"{new_product.name}_{new_product.id}_qr.png"
            image.save(str(settings.BASE_DIR)+'/media/qr/'+ filename)

            new_product.qr_code = '/qr/'+ filename

            new_product.save()
            form.save_m2m()

        return redirect("product_list")

    return render(request, "inventory/product_form.html", context={
        "form":form, 
        "create": True
    })

def product_update_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(instance=product)

    if request.method=="POST":
        form = ProductForm(request.POST, request.FILES, instance=Product.objects.get(pk=product_id))
        if form.is_valid():
            form.save()
            return redirect("product_list")

    return render(request, "inventory/product_form.html", context={
        "form":form, 
        "create": False,
        "product": product,
    })

def product_delete_view(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method=="POST":
        action_type = request.POST.get('action')
        if action_type=='confirm':
            product.delete()
        return redirect("product_list")
    
    return render(request, "inventory/product_delete.html", context={"product":product})

def product_restock_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = RestockForm()
    restocks = Restock.objects.filter(product=product).order_by('-date').values()

    if request.method=="POST":
        form = RestockForm(request.POST)
        if form.is_valid:
            restock = form.save(commit=False)
            restock.product = product
            product.quantity += restock.units
            product.save()
            restock.save()
            return redirect("product_list")

    return render(
        request, 
        "inventory/product_restock.html",
        context={
            "product" : product,
            "form" : form,
            "restocks" : restocks
        }
        )

def restock_order_view(request):
    sort_order = request.GET.get('order', 'asc')
    product_id = request.GET.get('product_id')
    product = Product.objects.get(pk=product_id)
    restocks = Restock.objects.filter(product=product).order_by(('-' if sort_order=='asc' else '') + 'date').values()

    return render(request, 'partials/restock_history.html',{'restocks':restocks, 'product_id' : product_id})

@role_required(['admin','manager'])
def category_view(request):
    categories = Category.objects.annotate(
        product_types=Count("product"),
        total_stock=Sum("product__quantity"),
        average_price=Avg("product__price")
    ).order_by("name")

    return render(
        request, 
        "inventory/category.html", 
        {
            'categories' : categories
        })

# def category_partial_view(request):
#     category_id = int(request.GET.get('category_id'))
#     products = Product.objects.all()

#     if category_id != -1:
#         category = Category.objects.get(pk=category_id)
#         products = Product.objects.filter(category=category)

#     return render(
#         request, 
#         "partials/category_partial.html", 
#         {
#             'products': products,
#         })

def category_form_view(request):
    form = CategoryForm()

    return render(
        request,
        'partials/category_form.html',
        context={
            'action' : 'Add',
            'form' : form,
            'redirect' : reverse('category_create')
        }
        )

def category_create_view(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid:
            form.save()
        
    return redirect('category')

def category_specific_view(request, category_id):
    category = Category.objects.annotate(
        product_types=Count("product"),
        total_stock=Sum("product__quantity"),
        average_price=Avg("product__price")
    ).get(pk=category_id)

    return render(
        request,
        'partials/category_specific.html',
        context={
            'category' : category
        }
    )

def category_delete_view(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method=="POST":
        action_type = request.POST.get('action')
        if action_type=="confirm":
            category.delete()
        
        return redirect('category')

    return render(
        request,
        'partials/category_delete.html',
        context={
            'category' : category
        }
    )

def category_edit_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    form = CategoryForm(instance=category)

    if request.method=="POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid:
            form.save()

        return redirect('category')
        
    return render(
        request,
        'partials/category_form.html',
        context={
            'action' : 'Edit',
            'form' : form,
            'redirect' : reverse('category_edit', args=[category_id])
        }
    )

def product_print_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    qr_code_path = Path(str(settings.BASE_DIR)+product.qr_code.url)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="qr_code_{product.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 50, f"QR Code for Product: {product.name}")

    p.drawImage(qr_code_path, x=width/2 - 25 * mm, y=height - 200, width=50 * mm, height=50 * mm)

    p.showPage()
    p.save()
    return response