from django.test import TestCase
from .models import OrderItem, Order, Coupon, User, Product


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.product = Product.objects.create(
            name="Test Product", price=10.0, discount_price=8.0
        )
        self.order_item = OrderItem.objects.create(
            user=self.user, item=self.product, quantity=2
        )

    def test_str_representation(self):
        self.assertEqual(str(self.order_item), "2 of Test Product")

    def test_total_item_price(self):
        self.assertEqual(self.order_item.get_total_item_price(), 20.0)

    def test_total_discount_item_price(self):
        self.assertEqual(self.order_item.get_total_discount_item_price(), 16.0)

    def test_amount_saved(self):
        self.assertEqual(self.order_item.get_amount_saved(), 4.0)

    def test_final_price_without_discount(self):
        self.product.discount_price = None
        self.product.save()
        self.assertEqual(self.order_item.get_final_price(), 20.0)

    def test_final_price_with_discount(self):
        self.assertEqual(self.order_item.get_final_price(), 16.0)


class CouponTestCase(TestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(code="TESTCODE", amount=5.0)

    def test_str_representation(self):
        self.assertEqual(str(self.coupon), "TESTCODE")

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.code, "TESTCODE")
        self.assertEqual(self.coupon.amount, 5.0)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.product1 = Product.objects.create(
            name="Product 1", price=10.0, discount_price=8.0
        )
        self.product2 = Product.objects.create(name="Product 2", price=15.0)
        self.order_item1 = OrderItem.objects.create(
            user=self.user, item=self.product1, quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            user=self.user, item=self.product2, quantity=1
        )
        self.order = Order.objects.create(user=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.order), "test_user")

    def test_get_total_without_coupon(self):
        self.order.items.add(self.order_item1, self.order_item2)
        self.assertEqual(self.order.get_total(), 35.0)

    def test_get_total_with_coupon(self):
        self.order.items.add(self.order_item1, self.order_item2)
        self.order.coupon = Coupon.objects.create(code="TESTCODE", amount=5.0)
        self.assertEqual(self.order.get_total(), 30.0)
