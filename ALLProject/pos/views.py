from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.urls import reverse
from .models import Product,CartItem,Cart,Payment,Employee
from .forms import ItemCodeForm, QuantityForm, CheckOutForm, ClearCartItems, ClearLastCartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def cashierPOSView(request):
    template = loader.get_template('pos/sales_cart.html')
    item_code_form = ItemCodeForm()
    quantity_form = QuantityForm()
    checkout_form = CheckOutForm()
    clear_cart_form = ClearCartItems()
    clear_last_form = ClearLastCartItem()
    product = None
    actual_quantity = None
    show_quantity = False
    cart_cost = 0.00

    if 'cart' not in request.session:
        request.session['cart'] = []
    if request.session['cart']:
        cart_cost = sum(item['total_price'] for item in request.session['cart'])
        print("Cart Cost = ",cart_cost)
        
    print(request.session['cart'])
    print("Request Session", request.session)
    print("Request Post: ",request.POST)
    
    if request.method == 'POST':
        # Handle submission for item code
        if 'item_code' in request.POST:
            #print("checking add product")
            item_code_form = ItemCodeForm(request.POST)
            if item_code_form.is_valid():
                item_code = item_code_form.cleaned_data['item_code']
                try:
                    product = Product.objects.get(id=item_code)
                    # if the same product exists in cart
                    actual_quantity = product.quantity
                    for items in request.session['cart']:
                      if str(item_code) == str(items['item_code']):
                        print("Item Found")
                        actual_quantity -= items['quantity']
                        print(actual_quantity)
                    messages.info(request, actual_quantity)
                    show_quantity = True
                except ObjectDoesNotExist:
                    messages.error(request, "ERROR: Product Not Found")
                    return HttpResponseRedirect(reverse('sales'))
        
        # Handle submission for product quantity
        if 'item_quantity' in request.POST:
            #print("checking add quantity")
            quantity_form = QuantityForm(request.POST)
            item_code = request.POST.get('item_code')
            if quantity_form.is_valid() and item_code:
                try:
                    product = Product.objects.get(id=item_code)
                    quantity = quantity_form.cleaned_data['item_quantity']

                    # Check if cart quantity is more than existing stock quantity
                    totalProduct = quantity
                    for items in request.session['cart']:
                      if item_code == items['item_code']:
                          totalProduct += items['quantity']

                    if totalProduct > product.quantity:
                        messages.error(request, "ERROR: Quantity exceeds available stock")
                        show_quantity = True
                    else:
                        # Show Warning alert if stock quantity reached alert_threshold
                        actual_quantity = product.quantity - totalProduct
                        if actual_quantity <= product.alert_threshold:
                            messages.error(request, "ALERT: LOW STOCK WARNING!")

                        # Add to cart logic
                        request.session['cart'].append({
                            'item_code' : item_code,
                            'name' : product.name,
                            'unit_price' : product.price,
                            'quantity' : quantity,
                            'total_price' : float(product.price*quantity)
                        })
                        request.session.modified = True

                        # reset forms and insert cart item successfully
                        item_code_form = ItemCodeForm()
                        quantity_form = QuantityForm()
                        item_code = None
                        quantity = None
                        product = None
                        show_quantity = False
                        return HttpResponseRedirect(reverse('sales'))
                    
                except ObjectDoesNotExist:
                    messages.error(request, "ERROR: Product Not Found")
                    return HttpResponseRedirect(reverse('sales'))

        # Handles Cart Items Deletion
        if 'clear_cart' in request.POST:
            request.session['cart'] = []
            request.session.modified = True
            messages.success(request, "Cleared All Items Added in Cart")
            return HttpResponseRedirect(reverse('sales'))

        if 'clear_last' in request.POST:
            if request.session['cart']:
                request.session['cart'].pop(-1)
                request.session.modified = True
                messages.success(request, "Cleared Last Item Added in Cart")
                return HttpResponseRedirect(reverse('sales'))
            else:
                messages.error(request, "ERROR: No Item in Cart")
                return HttpResponseRedirect(reverse('sales'))
        
        # Handles checkout submission
        if 'check_out' in request.POST:
            checkout_form = CheckOutForm(request.POST)
            print("Check-out")
            if checkout_form.is_valid():
                print("valid form")
                payment_method = checkout_form.cleaned_data['payment_method']
                print("Payment Method: ", payment_method)
                if request.session['cart']:
                    if payment_method == "cash" and checkout_form.cleaned_data['cashPaid'] < cart_cost:
                        messages.error(request, "ERROR: Cash amount is lower than cost of products")
                    else:
                        try:
                            change = cart_cost-checkout_form.cleaned_data['cashPaid']
                            # Create Cart Record
                            new_cart = Cart.objects.create(
                                total_cost=0.00,
                                payment_status=True)

                            # Create CartItems inside Cart
                            for items in request.session['cart']:
                                product = Product.objects.get(id=items['item_code'])
                                CartItem.objects.create(
                                    cart = new_cart, 
                                    product = product, 
                                    quantity = items['quantity'], 
                                    total_cost = items['total_price']
                                )
                                product.quantity -= items['quantity']
                                product.save()

                            # Payment Data
                            card_number = checkout_form.cleaned_data['card_number']
                            card_expiry = checkout_form.cleaned_data['expiry']
                            card_cvv = checkout_form.cleaned_data['cvv']

                            # Create and encrypt payment data
                            Payment.objects.create(
                                employeeID = Employee.objects.get(id=2),
                                payment_method = payment_method,
                                tax = 0.00,
                                discount = 0.00,
                                total_cost = cart_cost,
                                card_info = card_number,
                                expiry = card_expiry,
                                cvv = card_cvv,
                            )

                            new_cart.total_cost = cart_cost
                            new_cart.save()

                            if payment_method == 'debit_card':
                                messages.success(request, "Checkout Successful. Data saved.")
                            elif payment_method == 'cash':
                                messages.success(request, f"Checkout Successful. \nPlease return Change: RM {change*-1:.2f}")

                            # Clear Cart in session
                            print("finish adding cart")
                            request.session['cart'] = []
                            for key in list(request.session.keys()):
                                if not key.startswith("_"): # skip keys set by the django system
                                    del request.session[key]
                            request.session.modified = True
                            return HttpResponseRedirect(reverse('sales'))
                            
                        except ObjectDoesNotExist:
                            messages.error(request, "ERROR: One or more products in cart not found")
                            return HttpResponseRedirect(reverse('sales'))
                else:
                    print(checkout_form.errors)
                    messages.error(request, "ERROR: Cart is either empty or invalid checkout.")
                    return HttpResponseRedirect(reverse('sales'))

    context = {
        'item_code_form' : item_code_form,
        'quantity_form' : quantity_form,
        'checkout_form' : checkout_form,
        'clear_cart_form' : clear_cart_form,
        'clear_last_form' : clear_last_form,
        'product' : product,
        'actual_quantity' : actual_quantity if request.method == 'POST' else None,
        'item_code' : request.POST.get('item_code') if request.method == 'POST' else None,
        'cart' : request.session.get('cart',[]),
        'cart_cost' : cart_cost,
        'show_quantity' : show_quantity,
    }
    print(messages.get_messages)
    return HttpResponse(template.render(context,request))

def cashierHistoryView(request):
    template = loader.get_template('pos/view_history.html')
    context = {}
    return HttpResponse(template.render(context,request))