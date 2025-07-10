from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Employee

class EmployeeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_create_employee(self):
        employee = Employee.objects.create(user=self.user, role='cashier')
        self.assertEqual(employee.user.username, 'testuser')
        self.assertEqual(employee.role, 'cashier')
        self.assertTrue(employee.virgin_login)
        self.assertFalse(employee.active)

    def test_role_choices_valid(self):
        for valid_role in ['cashier', 'admin', 'manager']:
            employee = Employee(user=self.user, role=valid_role)
            # Should not raise error on full_clean
            try:
                employee.full_clean()
            except ValidationError:
                self.fail(f"Role '{valid_role}' should be valid")

    def test_role_invalid_choice(self):
        employee = Employee(user=self.user, role='invalid_role')
        with self.assertRaises(ValidationError):
            employee.full_clean()

    def test_user_delete_cascades_employee(self):
        employee = Employee.objects.create(user=self.user, role='manager')
        self.user.delete()
        self.assertEqual(Employee.objects.count(), 0)

    def test_one_user_one_employee(self):
        Employee.objects.create(user=self.user, role='admin')
        with self.assertRaises(Exception):
            Employee.objects.create(user=self.user, role='cashier')
