from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm
from django.conf import settings

import qrcode

# Create your views here.
@login_required
def product_list_view(request):
    products = Product.objects.all()
    product_id = request.GET.get("add")
    chosen_product = None
    filter_category = request.POST.get('category')
    default_category = "none"

    if product_id:
        chosen_product = Product.objects.get(pk=product_id)

    if request.method=="POST":
        if filter_category!="none":
            try:
                category_id = Category.objects.get(name=filter_category).id
            except Category.DoesNotExist:
                category_id = None
            products = Product.objects.filter(category=category_id)
            default_category = filter_category

        availability = request.POST.get('availability')

        if availability!="none":
            if(availability=="low"):
                products = Product.objects.filter(quantity__lte=10)
            elif(availability=="zero"):
                products = Product.objects.filter(quantity=0)
    
    return render(
        request,
        'inventory/product_list.html',
        context={
            'products':products,
            'product_count':len(products),
            'chosen_product': chosen_product,
            'default_category': default_category
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
        product.delete()
        return redirect("product_list")
    
    return render(request, "inventory/product_delete.html", context={"product":product})