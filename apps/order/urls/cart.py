from django.urls import path
from apps.order.views.api import AddToCartAPI, CartViewAPI,DeleteItemCart,UpdateItemCart


urlpatterns = [
    path("add-to-cart/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("cart/", CartViewAPI.as_view(), name="cart"),
    path("delete-product/",DeleteItemCart.as_view(),name="delete-product"),
    path("update-product/",UpdateItemCart.as_view(),name="update-product")
]
