from django.http import HttpResponse
from django.template import loader
from .models import Product,CartItem
from .forms import ItemCodeForm, QuantityForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def cashierPOSView(request):
    template = loader.get_template('pos/sales_cart.html')
    item_code_form = ItemCodeForm()
    quantity_form = QuantityForm()
    product = None
    error = None
    success = None
    show_quantity = False
    print("Opening POS system")

    if 'cart' not in request.session:
        request.session['cart'] = []
    print(f"{request.POST}")
    if request.method == 'POST':
        # Handle submission for item code
        if 'item_code' in request.POST:
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
            print("Quantity asked")
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
                        print("Product Added")
                        # Add to cart logic
                        request.session['cart'].append({
                            'item_code' : item_code,
                            'name' : product.name,
                            'quantity' : quantity,
                            'price' : float(product.price*quantity)
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
                    
                except ObjectDoesNotExist:
                    error = "ERROR: Product Not Found"
                    
        elif 'check_out' in request.POST:
            pass

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