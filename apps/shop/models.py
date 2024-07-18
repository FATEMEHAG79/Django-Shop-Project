from django.db import models
from utils.filename import maker
from django.template.defaultfilters import slugify
from apps.core.models import TimeStampMixin, LogicalMixin
from functools import partial
from django.core.validators import FileExtensionValidator


class Media(TimeStampMixin, LogicalMixin):
    position = models.PositiveIntegerField(null=False)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="media"
    )
    file = models.FileField(
        upload_to=partial(maker, "product"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "png", "jpg", "gif", "mp4", "avi", "flv"]
            )
        ],
    )

    class Meta:
        unique_together = ("product", "position")


class Category(LogicalMixin, TimeStampMixin):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="category", blank=False)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True
    )
    slug = models.SlugField(max_length=200, unique=True, editable=False)

    class Meta:
        unique_together = ("slug", "parent")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.title]
        relate = self.parent
        while relate is not None:
            full_path.append(relate.title)
            relate = relate.parent
        return "->".join(full_path[::-1])


class Brand(LogicalMixin, TimeStampMixin):
    name = models.CharField(max_length=80)
    image = models.ImageField(upload_to="brands")
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    country = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(LogicalMixin, TimeStampMixin):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category", null=True
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="brand", null=True
    )
    quantity = models.IntegerField()
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField(default=0)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    discount_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.slug

    def deactivate(self):
        if self.quantity == 0:
            self.is_active = False
            self.save(update_fields=["is_active"])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def can_be_added_to_cart(self):
        return self.is_active


class Comment(LogicalMixin, TimeStampMixin):
    name = models.CharField(max_length=150)
    text = models.CharField(max_length=150)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comment"
    )
