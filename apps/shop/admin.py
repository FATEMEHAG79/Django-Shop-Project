from django.contrib import admin
from .models import Category, Product, Comment, Brand, Media

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(Brand)
