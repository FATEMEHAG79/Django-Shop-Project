from apps.shop.views import template
from django.urls import path

urlpatterns = [
    path(
        "shop/<str:slug>/", template.CategoryDetailView.as_view(), name="categorydetail"
    ),
    path(
        "shop/<str:slug>/<str:slug1>",
        template.SubCategoryDetailView.as_view(),
        name="subcategorydetail",
    ),
    path(
        "shop/product/<str:slug>/<str:slug1>",
        template.ProductDetailView.as_view(),
        name="productdetail",
    ),
    path(
        "comment/<str:slug>",
        template.AddComment.as_view(),
        name="comment",
    ),
]
