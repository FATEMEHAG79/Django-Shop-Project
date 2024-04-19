from django.test import TestCase
from .models import Category, Product


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title="Test Category", slug="test-category")

    def test_title_content(self):
        category = Category.objects.get(id=1)
        expected_object_name = f"{category.title}"
        self.assertEqual(expected_object_name, "Test Category")

    def test_slug(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.slug, "test-category")


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title="Test Category", slug="test-category")
        category = Category.objects.get(id=1)
        Product.objects.create(
            category=category, name="Test Product", slug="test-product"
        )

    def test_name_content(self):
        product = Product.objects.get(id=1)
        expected_object_name = f"{product.name}"
        self.assertEqual(expected_object_name, "Test Product")

    def test_slug(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.slug, "test-product")
