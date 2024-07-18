from django.views import generic
from django.views.generic import DetailView
from apps.shop.models import Product, Category, Media, Comment
from django.shortcuts import render, redirect


class CategoryDetailView(DetailView):
    model = Product, Category

    def get(self, request, slug):
        itemcategory = Category.objects.filter(parent__slug=slug)
        productlist = Product.objects.select_related("category__parent").filter(
            category__parent__slug=slug
        )
        media_file = Media.objects.filter(product__category__parent__slug=slug)
        context = {
            "itemcategory": itemcategory,
            "productlist": productlist,
            "media": media_file,
        }

        return render(request, "product/category-detail.html", context)


class SubCategoryDetailView(DetailView):
    model = Product, Category

    def get(self, request, slug, slug1):
        productlist = Product.objects.select_related("category").filter(
            category__slug=slug1
        )
        media_file = Media.objects.filter(product__category__parent__slug=slug)
        content = {
            "productlist": productlist,
            "media": media_file,
        }

        return render(request, "product/subcategory_detail.html", content)


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, slug, slug1):
        product = Product.objects.get(slug=slug1)
        media_file = Media.objects.filter(product__slug=slug1)
        comments = Comment.objects.filter(product__slug=slug1, is_active=True)
        content = {"product": product, "media": media_file, "comment": comments}
        return render(request, "product/product_detail.html", content)


class AddComment(generic.RedirectView):
    def get(self, request, slug):
        return render(request, "product/product_detail.html")

    def post(self, request, slug):
        name = self.request.POST.get("name")
        txt = self.request.POST.get("txt")
        product = Product.objects.get(slug=slug)
        comment = Comment.objects.create(name=name, text=txt, product=product)
        comment.save()
        return redirect("home")
