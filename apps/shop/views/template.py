from django.views.generic import DetailView
from apps.shop.models import Product,Category,Brand
from django.shortcuts import render


class CategoryDetailView(DetailView):
    model = Product,Category

    def get(self, request,slug):
        itemcategory = Category.objects.filter(parent__slug=slug)
        productlist = Product.objects.select_related("category__parent").filter(category__parent__slug=slug)
        category = Category.objects.filter(parent=None)
        brands= Brand.objects.all()
        context={
            "itemcategory":itemcategory,
            "productlist": productlist,
            "category": category,
            "brands":brands
        }

        return render(request,"product/category-detail.html",context)



class SubCategoryDetailView(DetailView):
    model = Product,Category
    def get(self, request,slug,slug1):
        productlist = Product.objects.select_related("category").filter(category__slug=slug1)
        category = Category.objects.filter(parent=None)
        brands= Brand.objects.all()
        content={
            "productlist": productlist,
            "category": category,
            "brands":brands
        }

        return render(request,"product/subcategory_detail.html",content)



class ProductDetailView(DetailView):
    model = Product
    def get(self, request,slug,slug1):
        product = Product.objects.get(slug=slug1)
        category = Category.objects.filter(parent=None)
        content={
            "product":product,
            "category": category,
        }

        return render(request,"product/product_detail.html",content)