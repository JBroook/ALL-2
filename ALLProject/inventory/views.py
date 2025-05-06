from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Category

# Create your views here.
@login_required
def product_list_view(request):
    return render(request, 'inventory/product_list.html')

def product_list_view2(request):
    products = Product.objects.all()
    product_id = request.GET.get("add")
    chosen_product = None
    default_category = "none"

    if product_id:
        chosen_product = Product.objects.get(pk=product_id)

    if request.method=="POST":
        if request.POST.get('category')!="none":
            try:
                category_id = Category.objects.get(name=request.POST.get('category')).id
            except Category.DoesNotExist:
                category_id = None
            products = Product.objects.filter(category=category_id)
            default_category = request.POST.get('category')

        availability = request.POST.get('availability')

        if availability!="none":
            if(availability=="low"):
                products = Product.objects.filter(quantity__lte=10)
            elif(availability=="zero"):
                products = Product.objects.filter(quantity=0)
    
    return render(
        request,
        'inventory/product_list2.html',
        context={
            'products':products,
            'product_count':len(products),
            'chosen_product': chosen_product,
            'default_category': default_category
        }
    )