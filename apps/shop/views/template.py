from django.views.generic import DetailView
from apps.shop.models import Product, Category, Brand,Media
from django.shortcuts import render


class CategoryDetailView(DetailView):
    model = Product, Category

    def get(self, request, slug):
        itemcategory = Category.objects.filter(parent__slug=slug)
        productlist = Product.objects.select_related("category__parent").filter(
            category__parent__slug=slug
        )
        media_file= Media.objects.filter(product__category__parent__slug=slug)
        if "cart_data_obj" in request.session:
            totalcartitems = sum(
                item["qty"] for item in request.session["cart_data_obj"].values()
            )
        else:
            totalcartitems = 0
        category = Category.objects.filter(parent=None)
        brands = Brand.objects.all()
        context = {
            "itemcategory": itemcategory,
            "productlist": productlist,
            "category": category,
            "brands": brands,
            "media" :media_file,
            "totalcartitems": totalcartitems,
        }

        return render(request, "product/category-detail.html", context)


class SubCategoryDetailView(DetailView):
    model = Product, Category

    def get(self, request, slug, slug1):
        productlist = Product.objects.select_related("category").filter(
            category__slug=slug1
        )
        media_file = Media.objects.filter(product__category__parent__slug=slug)
        if "cart_data_obj" in request.session:
            totalcartitems = sum(
                item["qty"] for item in request.session["cart_data_obj"].values()
            )
        else:
            totalcartitems = 0
        category = Category.objects.filter(parent=None)
        brands = Brand.objects.all()
        content = {
            "productlist": productlist,
            "category": category,
            "brands": brands,
            "media": media_file,
            "totalcartitems": totalcartitems,
        }

        return render(request, "product/subcategory_detail.html", content)


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, slug, slug1):
        product = Product.objects.get(slug=slug1)
        category = Category.objects.filter(parent=None)
        media_file = Media.objects.filter(product__slug=slug1)
        if "cart_data_obj" in request.session:
            totalcartitems = sum(
                item["qty"] for item in request.session["cart_data_obj"].values()
            )
        else:
            totalcartitems = 0
        content = {
            "product": product,
            "category": category,
            "media": media_file,
            "totalcartitems": totalcartitems,
        }

        return render(request, "product/product_detail.html", content)
