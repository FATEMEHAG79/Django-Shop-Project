from django.test import TestCase
from .models import Order, OrderItem, Product, User


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", email="test@example.com")
        self.order = Order.objects.create(user=self.user)

    def test_order_total_calculation(self):
        product1 = Product.objects.create(name="Product 1", price=10.0)
        product2 = Product.objects.create(name="Product 2", price=20.0)

        order_item1 = OrderItem.objects.create(
            item=product1, quantity=2, order=self.order
        )
        order_item2 = OrderItem.objects.create(
            item=product2, quantity=3, order=self.order
        )

        expected_total = (product1.price * order_item1.quantity) + (
            product2.price * order_item2.quantity
        )
        self.assertEqual(self.order.get_total(), expected_total)


class OrderitemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", email="test@example.com")

        self.product = Product.objects.create(name="Test Product", price=10.0)

        self.order = Order.objects.create(user=self.user)

        self.order_item = OrderItem.objects.create(
            item=self.product, quantity=2, order=self.order
        )

    def test_order_total(self):
        expected_total = 20.0
        self.assertEqual(self.order.get_total(), expected_total)

    def test_order_str(self):
        expected_str = self.user.username
        self.assertEqual(str(self.order), expected_str)
