from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, Restock
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

class CategoryModelTests(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")
        self.assertEqual(Category.objects.count(), 1)

    def test_category_name_required(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name=None)

class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")

        # Dummy image files for ImageFields
        self.dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.dummy_qr = SimpleUploadedFile(name='test_qr.jpg', content=b'', content_type='image/jpeg')
        self.dummy_barcode = SimpleUploadedFile(name='test_barcode.jpg', content=b'', content_type='image/jpeg')

    def test_create_product_minimal(self):
        product = Product.objects.create(
            name="Smartphone",
            quantity=10,
            image=self.dummy_image,
            supplier="ABC Corp",
            category=self.category,
            price=299.99,
            alert_threshold=5,
            qr_code=self.dummy_qr,
            barcode_number="1234567890",
            barcode_img=self.dummy_barcode,
            sku="SP001"
        )
        self.assertEqual(product.name, "Smartphone")
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.supplier, "ABC Corp")
        self.assertEqual(product.category.name, "Electronics")
        self.assertEqual(product.price, 299.99)
        self.assertEqual(product.alert_threshold, 5)
        self.assertEqual(product.barcode_number, "1234567890")
        self.assertEqual(product.sku, "SP001")
        self.assertIsNotNone(product.timeStamp)

    def test_barcode_number_uniqueness(self):
        Product.objects.create(
            name="Item1",
            quantity=5,
            image=self.dummy_image,
            supplier="Supplier1",
            category=self.category,
            price=100.0,
            alert_threshold=2,
            qr_code=self.dummy_qr,
            barcode_number="UNIQUE123",
            barcode_img=self.dummy_barcode,
            sku="SKU001"
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Item2",
                quantity=3,
                image=self.dummy_image,
                supplier="Supplier2",
                category=self.category,
                price=50.0,
                alert_threshold=1,
                qr_code=self.dummy_qr,
                barcode_number="UNIQUE123",  # duplicate barcode
                barcode_img=self.dummy_barcode,
                sku="SKU002"
            )

    def test_quantity_cannot_be_negative(self):
        product = Product(
            name="Negative Quantity",
            quantity=-1,
            image=self.dummy_image,
            supplier="SupplierX",
            category=self.category,
            price=10.0,
            alert_threshold=1,
            qr_code=self.dummy_qr,
            sku="SKU003"
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_alert_threshold_cannot_be_negative(self):
        product = Product(
            name="Negative Alert",
            quantity=5,
            image=self.dummy_image,
            supplier="SupplierY",
            category=self.category,
            price=20.0,
            alert_threshold=-5,
            qr_code=self.dummy_qr,
            sku="SKU004"
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_price_must_be_positive(self):
        product = Product(
            name="Negative Price",
            quantity=5,
            image=self.dummy_image,
            supplier="SupplierZ",
            category=self.category,
            price=-100.0,
            alert_threshold=2,
            qr_code=self.dummy_qr,
            sku="SKU005"
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_sku_max_length(self):
        product = Product(
            name="Long SKU",
            quantity=5,
            image=self.dummy_image,
            supplier="SupplierLong",
            category=self.category,
            price=10.0,
            alert_threshold=1,
            qr_code=self.dummy_qr,
            sku="TOO_LONG_SKU_12345"
        )
        with self.assertRaises(ValidationError):
            product.full_clean()


class RestockModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.product = Product.objects.create(
            name="Apple",
            quantity=50,
            image=self.dummy_image,
            supplier="Supplier A",
            category=self.category,
            price=0.5,
            alert_threshold=10,
            qr_code=self.dummy_image,
            sku="APL123"
        )

    def test_create_restock(self):
        restock = Restock.objects.create(
            product=self.product,
            date=timezone.now().date(),
            units=20,
            cpu=0.3
        )
        self.assertEqual(restock.product, self.product)
        self.assertEqual(restock.units, 20)
        self.assertEqual(restock.cpu, 0.3)

    def test_units_must_be_positive(self):
        restock = Restock(
            product=self.product,
            date=timezone.now().date(),
            units=-5,
            cpu=0.2
        )
        with self.assertRaises(ValidationError):
            restock.full_clean()

    def test_cpu_must_be_positive(self):
        restock = Restock(
            product=self.product,
            date=timezone.now().date(),
            units=10,
            cpu=-1.0
        )
        with self.assertRaises(ValidationError):
            restock.full_clean()

    def test_date_defaults_to_today(self):
        restock = Restock.objects.create(
            product=self.product,
            units=15,
            cpu=0.4
        )
        self.assertAlmostEqual(restock.date, timezone.now())

    def test_restock_without_product_fails(self):
        with self.assertRaises(IntegrityError):
            Restock.objects.create(
                product=None,
                units=10,
                cpu=0.5,
                date=timezone.now().date()
            )

    def test_stock_quantity_updates_on_restock(self):
        initial_qty = self.product.quantity
        units_added = 30
        restock = Restock.objects.create(
            product=self.product,
            units=units_added,
            cpu=0.25,
            date=timezone.now().date()
        )
        restock.change_quantity()
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, initial_qty + units_added)
