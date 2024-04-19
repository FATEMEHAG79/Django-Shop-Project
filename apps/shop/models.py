from django.db import models
from django.template.defaultfilters import slugify
from apps.user.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="media", blank=False)
    sub_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        null=True,
        blank=True,
    )
    is_actived = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", null=True
    )
    image = models.ImageField(upload_to="media")
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    is_actived = models.BooleanField(default=True)
    discount_price = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def can_be_added_to_cart(self):
        return self.is_actived


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=150)
    date_text = models.DateTimeField(auto_now=True)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
