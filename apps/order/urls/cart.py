from django.urls import path
from apps.order.views.api import AddToCartAPI


urlpatterns = [path("add-to-cart/", AddToCartAPI.as_view(), name="add-to-cart")]
