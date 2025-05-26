from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Product,CartItem,Cart
from .forms import ItemCodeForm, QuantityForm, CheckOutForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def cashierPOSView(request):
    template = loader.get_template('pos/sales_cart.html')
    item_code_form = ItemCodeForm()
    quantity_form = QuantityForm()
    checkout_form = CheckOutForm()
    product = None
    error = None
    success = None
    show_quantity = False

    if 'cart' not in request.session:
        request.session['cart'] = []
    print(request.session['cart'])
    print(request.POST)
    
    if request.method == 'POST':
        # Handle submission for item code
        if 'item_code' in request.POST:
            print("checking add product")
            item_code_form = ItemCodeForm(request.POST)
            if item_code_form.is_valid():
                item_code = item_code_form.cleaned_data['item_code']
                try:
                    product = Product.objects.get(id=item_code)
                    show_quantity = True
                except ObjectDoesNotExist:
                    error = "ERROR: Product Not Found"
        
        # Handle submission for product quantity
        if 'item_quantity' in request.POST:
            print("checking add quantity")
            quantity_form = QuantityForm(request.POST)
            item_code = request.POST.get('item_code')
            if quantity_form.is_valid() and item_code:
                try:
                    product = Product.objects.get(id=item_code)
                    quantity = quantity_form.cleaned_data['item_quantity']
                    if quantity > product.quantity:
                        error = "ERROR: Quantity exceeds available stock."
                        show_quantity = True
                    else:
                        # Add to cart logic
                        request.session['cart'].append({
                            'item_code' : item_code,
                            'name' : product.name,
                            'unit_price' : product.price,
                            'quantity' : quantity,
                            'total_price' : float(product.price*quantity)
                        })
                        request.session.modified = True # Ensure session saved

                        # reset forms and insert cart item successfully
                        success = f"{quantity} of {product.name} added to cart."
                        item_code_form = ItemCodeForm()
                        quantity_form = QuantityForm()
                        item_code = None
                        quantity = None
                        product = None
                        show_quantity = False
                        return HttpResponseRedirect(reverse('sales'))
                    
                except ObjectDoesNotExist:
                    error = "ERROR: Product Not Found"
        
        # Handles checkout submission
        if 'check_out' in request.POST:
            checkout_form = CheckOutForm(request.POST)
            print("Check-out")
            if checkout_form.is_valid():
                print("valid form")
                if request.session['cart']:
                    try:
                        new_cart = Cart.objects.create(
                            total_cost=0.00,
                            payment_status=False)
                        total_cart_cost = 0.0

                        for items in request.session['cart']:
                            product = Product.objects.get(id=items['item_code'])
                            CartItem.objects.create(
                                cart=new_cart, 
                                product=product, 
                                quantity=items['quantity'], 
                                total_cost=items['total_price']
                            )
                            total_cart_cost += items['total_price']

                        new_cart.total_cost = total_cart_cost
                        new_cart.save()

                        # Clear Cart in session
                        print("finish adding cart")
                        request.session['cart'] = []
                        request.session.modified = True

                        success = "Checkout Successful. Fata saved."
                        return HttpResponseRedirect(reverse('sales'))
                        
                    except ObjectDoesNotExist:
                        error = "ERROR: One or more products in cart not found"
            else:
                error = "ERROR: Cart is either empty or invalid checkout."
        else:
            print("Checkout form invalid: ", checkout_form.errors)
            error = "ERROR: Invalid CheckOut Form."

    context = {
        'item_code_form' : item_code_form,
        'quantity_form' : quantity_form,
        'product' : product,
        'error' : error,
        'success' : success,
        'item_code' : request.POST.get('item_code') if request.method == 'POST' else None,
        'cart' : request.session.get('cart',[]),
        'show_quantity' : show_quantity,
    }
    return HttpResponse(template.render(context,request))

def cashierHistoryView(request):
    template = loader.get_template('pos/view_history.html')
    context = {}
    return HttpResponse(template.render(context,request))