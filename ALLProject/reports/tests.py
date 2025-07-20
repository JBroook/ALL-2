from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from inventory.models import Product, Category
from pos.models import Cart, CartItem, Payment
from users.models import Employee
from freezegun import freeze_time
from datetime import datetime, timedelta
import json

# Create your tests here.
class ReportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('cashier1', 'cashier@test.com', 'pass')
        self.user.is_staff = False
        self.user.save()
        employee = Employee.objects.create(role="cashier", user_id=self.user.id, virgin_login=0)
        cat = Category.objects.create(name="Coding Book")
        
        self.product1 = Product.objects.create(
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
        self.product2 = Product.objects.create(
            id=2,
            name="Advanced Django",
            quantity=5,
            supplier="Coventry",
            category=cat,
            price=30.00,
            alert_threshold=3,
            sku="def456",
            timeStamp=timezone.now()
        )

        # Define dates for testing
        self.date1 = datetime(2025, 7, 6, tzinfo=timezone.get_current_timezone())
        self.date2 = datetime(2025, 7, 5, tzinfo=timezone.get_current_timezone())
        
        # Cart and Payment for date1
        with freeze_time(self.date1):
            cart1 = Cart.objects.create(total_cost=24.50, payment_status=True)
            CartItem.objects.create(cart=cart1, product=self.product1, quantity=1, total_cost=24.50)
            Payment.objects.create(cart=cart1, employeeID=employee, payment_method="Cash", total_cost=24.50)

        with freeze_time(self.date2):
            cart2 = Cart.objects.create(total_cost=54.50, payment_status=True)
            CartItem.objects.create(cart=cart2, product=self.product1, quantity=1, total_cost=24.50)
            CartItem.objects.create(cart=cart2, product=self.product2, quantity=1, total_cost=30.00)
            Payment.objects.create(cart=cart2, employeeID=employee, payment_method="Card", total_cost=54.50)
    
        self.date3 = datetime(2025, 5, 5, tzinfo=timezone.get_current_timezone())
        with freeze_time(self.date3):
            cart3 = Cart.objects.create(total_cost=49.00, payment_status=True)
            CartItem.objects.create(cart=cart3, product=self.product1, quantity=3, total_cost=73.50)
            Payment.objects.create(cart=cart3, employeeID=employee, payment_method="Card", total_cost=73.50)
    

    def test_daily_transactions_query(self):
        daily_transactions = Payment.objects.filter(timeStamp=self.date1)
        self.assertEqual(daily_transactions.count(), 1)
        self.assertEqual(daily_transactions[0].total_cost, 24.50)
        
        daily_transactions = Payment.objects.filter(timeStamp=self.date2)
        self.assertEqual(daily_transactions.count(), 1)
        self.assertEqual(daily_transactions[0].total_cost, 54.50)

    def test_monthly_transactions(self):
        monthly_transactions = Payment.objects.filter(timeStamp__month=self.date1.month)
        self.assertEqual(monthly_transactions.count(), 2)
        self.assertEqual(monthly_transactions[0].total_cost, 24.50)
        self.assertEqual(monthly_transactions[1].total_cost, 54.50)

    def test_yearly_sold_of_product(self):
        product1 = Product.objects.get(id=1)
        yearly_sold = []
        for i in range(1,13):
            items = CartItem.objects.filter(cart__timeStamp__month=i).filter(product=product1).aggregate(quantity=Sum('quantity'))

            if items['quantity'] is None:
                yearly_sold.append({'quantity':0})
            else:
                yearly_sold.append(items)
        
        self.assertEqual(yearly_sold[4]['quantity'], 3) # 3 Books Sold
        self.assertEqual(yearly_sold[6]['quantity'], 2) # 2 Book Sold