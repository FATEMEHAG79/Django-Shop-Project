from django.test import TestCase
from .models import User, Address


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="Test@123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("Test@123"))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com", username="admin", password="Admin@123"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)


class AddressModelTest(TestCase):
    def test_address_creation(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="Test@123"
        )
        address = Address.objects.create(
            user=user,
            province="tehran",
            apartment_address="Test address",
            zip="1234567890",
        )
        self.assertEqual(address.user, user)
        self.assertEqual(address.province, "tehran")
        self.assertEqual(address.apartment_address, "Test address")
        self.assertEqual(address.zip, "1234567890")
