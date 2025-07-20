from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from inventory.models import Product, Category
from pos.models import Cart, CartItem, Payment
from users.models import Employee

# Create your tests here.
class POSTest(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()
        employee = Employee.objects.create(role="cashier",user_id=self.adminuser.id,virgin_login=0)
        cat = Category.objects.create(name="Coding Book")
        dummy = Product.objects.create(
                    id=1,
                    name="Introduction To Python",
                    quantity=10,
                    supplier="Coventry",
                    category=cat,
                    price=24.50,
                    alert_threshold=5,
                    sku="abc123",
                    timeStamp=timezone.now()
                    )
        cart = Cart.objects.create(payment_status=True)
        CartItem.objects.create(
            id=1,
            cart=cart,
            product=dummy,
            quantity=2,
            total_cost=49.00,
        )
        cart.total_cost = cart.get_cart_total()
        cart.save()
        Payment.objects.create(
            cart=cart,
            employeeID=employee,
            payment_method="Cash",
            total_cost=cart.get_cart_total()
        )

    def test_cart(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.total_cost, 49.00)

    def test_product_in_cart(self):
        cart = Cart.objects.get(id=1)
        items_in_cart = CartItem.objects.filter(cart=cart).first()

        if items_in_cart is None:
            self.fail("No CartItem found")

        self.assertEqual(items_in_cart.product.name,"Introduction To Python")
        
    def test_payment(self):
        product = Product.objects.get(id=1)
        items_in_cart = CartItem.objects.filter(product__name=product.name).first()
        paid = Payment.objects.get(cart=items_in_cart.cart)

        self.assertEqual(paid.total_cost, 49.00)
        self.assertEqual(paid.payment_method, "Cash")