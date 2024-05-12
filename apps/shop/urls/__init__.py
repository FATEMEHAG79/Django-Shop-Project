from django.urls import path, include

urlpatterns = [
    path("", include("apps.shop.urls.product")),
]
