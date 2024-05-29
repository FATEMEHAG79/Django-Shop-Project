from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.order.models import Product
from apps.shop.models import Media


class AddToCartAPI(APIView):
    def get(self, request, *args, **kwargs):
        cart_product = {
            str(request.GET["id"]): {
                "name": request.GET["name"],
                "qty": int(request.GET["qty"]),
                "price": request.GET["price"],
            }
        }
        if "cart_data_obj" in request.session:
            cart_data = request.session["cart_data_obj"]
            if str(request.GET["id"]) in cart_data:
                cart_data[str(request.GET["id"])]["qty"] += int(request.GET["qty"])
                cart_data.update(cart_data)
                request.session["cart_data_obj"] = cart_data
            else:
                cart_data = request.session["cart_data_obj"]
                cart_data.update(cart_product)
                request.session["cart_data_obj"] = cart_data
        else:
            request.session["cart_data_obj"] = cart_product
        return Response(
            {
                "data": request.session["cart_data_obj"],
                "totalcartitems": sum(
                    item["qty"] for item in request.session["cart_data_obj"].values()
                ),
            }
        )


class CartViewAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/cart.html"
    def get(self, request):
        cart_total_amount = 0
        if len(request.session["cart_data_obj"]):
            cart_data = request.session["cart_data_obj"]
            for p_id, item in cart_data.items():
                item["totla_price"]=int(item["qty"]) * float(item["price"])
                product=Product.objects.get(id=p_id)
                item["slug_category"]=product.category.slug
                item["slug"] = product.slug
                cart_total_amount += int(item["qty"]) * float(item["price"])
            cart_data = request.session["cart_data_obj"]
            total_cart_items = sum(
                item["qty"] for item in request.session["cart_data_obj"].values()
            )
            return Response(
                {
                    "cart_data": cart_data,
                    "total_cart_items": total_cart_items,
                    "cart_total_amount": cart_total_amount,
                }
            )
        else:
            return render(request, template_name="cart/cart-empty.html")



class DeleteItemCart(APIView):
    def get(self, request):
        item_id=str(request.GET["id_item"])
        if "cart_data_obj" in request.session:
            if item_id in request.session["cart_data_obj"]:
                cart_data=request.session["cart_data_obj"]
                del request.session["cart_data_obj"][item_id]
                request.session["cart_data_obj"]=cart_data
        cart_total_amount = 0
        if "cart_data_obj" in request.session:
            cart_data = request.session["cart_data_obj"]
            for p_id, item in cart_data.items():
                item["totla_price"] = int(item["qty"]) * float(item["price"])
                product = Product.objects.get(id=p_id)
                item["slug_category"] = product.category.slug
                item["slug"] = product.slug
                media_files = Media.objects.filter(product=product)
                item["media"] = [{"url":media.file.url}for media in media_files]
                cart_total_amount += int(item["qty"]) * float(item["price"])
            cart_data = request.session["cart_data_obj"]
            total_cart_items = sum(
                item["qty"] for item in request.session["cart_data_obj"].values()
            )
            context=render_to_string("cart/cart_list.html", {
                    "cart_data": cart_data,
                    "total_cart_items": total_cart_items,
                    "cart_total_amount": cart_total_amount,
                })
            return Response(
                {
                    "data" : context,
                    "totalcartitems": sum(
                    item["qty"] for item in request.session["cart_data_obj"].values()),
                    "cart_total_amount": cart_total_amount,
                }
            )
        else:
            return render(request, template_name="cart/cart-empty.html")

