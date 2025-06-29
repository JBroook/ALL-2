from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Restock
from .forms import ProductForm, RestockForm, CategoryForm
from django.conf import settings
from django.db.models import Count, Avg, Sum, Prefetch
from django.urls import reverse
from users.decorators import role_required
from django.contrib import messages

from django.http import HttpResponse


@role_required(['admin','manager'])
def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by("name")
    page = "nav-inventory"

    return render(
        request,
        'inventory/product_list.html',
        context={
            'products' : products,
            'product_count': len(products),
            'categories' : categories,
            'page': page
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

    page = "nav-inventory"
    
    return render(
        request,
        'partials/product_list_partial.html',
        context={
            'products' : products,
            'page': page
        }
    )

def product_info_view(request, product_id):
    product = Product.objects.get(pk=product_id)
        
    page = "nav-inventory"

    return render(
        request,
        'partials/product_info.html',
        context={
            'chosen_product' : product,
            'page': page
        }
    )

def product_create_view(request):
    form = ProductForm()
    page = "nav-inventory"

    if request.method=="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.category = form.cleaned_data["category"] 

            new_product.save()
            form.save_m2m()

        messages.add_message(request, messages.SUCCESS, "Product added!")
        
        return redirect("product_list")

    return render(request, "inventory/product_form.html", context={
        "form":form, 
        "create": True,
        'page': page
    })

def product_update_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(instance=product)
        
    page = "nav-inventory"

    if request.method=="POST":
        form = ProductForm(request.POST, request.FILES, instance=Product.objects.get(pk=product_id))
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, "Product updated!")
        else:
            messages.add_message(request, messages.ERROR, "Failed!")

        return redirect("product_list")

    return render(request, "inventory/product_form.html", context={
        "form":form, 
        "create": False,
        "product": product,
        'page': page
    })

def product_delete_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    page = "nav-inventory"

    if request.method=="POST":
        action_type = request.POST.get('action')
        if action_type=='confirm':
            try:
                product.delete()
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Cannot delete!")
            else:
                messages.add_message(request, messages.SUCCESS, "Product deleted!")
        return redirect("product_list")
    
    return render(request, "inventory/product_delete.html", context={"product":product,'page':page})

def product_restock_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = RestockForm()
    restocks = Restock.objects.filter(product=product).order_by('-date').values()
        
    page = "nav-inventory"

    if request.method=="POST":
        form = RestockForm(request.POST)
        if form.is_valid:
            restock = form.save(commit=False)
            restock.product = product
            product.quantity += restock.units
            product.save()
            restock.save()
            messages.add_message(request, messages.SUCCESS, "Product restocked!")
            return redirect("product_list")

    return render(
        request, 
        "inventory/product_restock.html",
        context={
            "product" : product,
            "form" : form,
            "restocks" : restocks,
            'page': page
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
    ).prefetch_related(
        Prefetch("product_set", queryset=Product.objects.all(), to_attr="products")
    ).order_by("name")
        
    page = "nav-category"

    return render(
        request, 
        "inventory/category.html", 
        {
            'categories' : categories,
            'page': page
        })

def category_partial_view(request):
    sort_method = request.GET.get('sort')

    categories = Category.objects.annotate(
        product_types=Count("product"),
        total_stock=Sum("product__quantity"),
        average_price=Avg("product__price"),
    ).prefetch_related(
        Prefetch("product_set", queryset=Product.objects.all(), to_attr="products")
    ).order_by(sort_method)

    return render(
        request, 
        "partials/category_partial.html", 
        {
            'categories' : categories
        })

def category_form_view(request):
    form = CategoryForm()
    page = "nav-category"

    return render(
        request,
        'partials/category_form.html',
        context={
            'action' : 'Add',
            'form' : form,
            'redirect' : reverse('category_create'),
            'page': page
        }
        )

def category_create_view(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category added!")
        else:
            messages.add_message(request, messages.ERROR, "Failed!")
    return redirect('category')

def category_specific_view(request, category_id):
    category = Category.objects.annotate(
        product_types=Count("product"),
        total_stock=Sum("product__quantity"),
        average_price=Avg("product__price")
    ).get(pk=category_id)
        
    page = "nav-category"

    return render(
        request,
        'partials/category_specific.html',
        context={
            'category' : category,
            'page': page
        }
    )

def category_delete_view(request, category_id):
    category = Category.objects.get(pk=category_id)
        
    page = "nav-category"

    if request.method=="POST":
        action_type = request.POST.get('action')
        if action_type=="confirm":
            category.delete()
            messages.add_message(request, messages.SUCCESS, "Category deleted!")
        
        return redirect('category')

    return render(
        request,
        'partials/category_delete.html',
        context={
            'category' : category,
            'page': page
        }
    )

def category_edit_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    form = CategoryForm(instance=category)
    page = "nav-category"

    if request.method=="POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category updated!")
        else:
            messages.add_message(request, messages.ERROR, "Failed!")

        return redirect('category')
        
    return render(
        request,
        'partials/category_form.html',
        context={
            'action' : 'Edit',
            'form' : form,
            'redirect' : reverse('category_edit', args=[category_id]),
            'page': page
        }
    )

def product_print_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    return product.print_codes()
