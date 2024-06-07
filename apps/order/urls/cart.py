from django.urls import path
from apps.order.views.api import AddToCartAPI, CartViewAPI,DeleteItemCart,UpdateItemCart,Checkout,EditAddress,PlaceOrderView,ConfirmOrderView




urlpatterns = [
    path("add-to-cart/", AddToCartAPI.as_view(), name="add-to-cart"),
    path("cart/", CartViewAPI.as_view(), name="cart"),
    path("delete-product/",DeleteItemCart.as_view(),name="delete-product"),
    path("update-product/",UpdateItemCart.as_view(),name="update-product"),
    path("checkout/<str:slug>/",Checkout.as_view(),name="checkout"),
    path("checkout/", EditAddress.as_view(), name="editaddress"),
    path("order-end/",PlaceOrderView.as_view(),name="order"),
    path("orderconfirm/<int:id>",ConfirmOrderView.as_view(),name="order-confirm"),
    # path("checkout/", CreateAddress.as_view(), name="createaddress"),
]
