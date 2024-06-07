from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.order.models import Order,OrderItem,Product
from apps.user.models import Address,User
from apps.order.serializers import AdressSerialiser
from rest_framework.permissions import IsAuthenticated
from apps.shop.models import Media
from django.shortcuts import redirect


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



class UpdateItemCart(APIView):
    def get(self, request):
        item_id=str(request.GET["id"])
        item_qty=int(request.GET["qty"])
        if "cart_data_obj" in request.session:
            if item_id in request.session["cart_data_obj"]:
                cart_data=request.session["cart_data_obj"]
                cart_data[str(request.GET["id"])]["qty"]=item_qty
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




class Checkout(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/checkout.html"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if len(request.session.get("cart_data_obj", [])):
            user = request.user
            address = Address.objects.filter(user=user)
            serializer = AdressSerialiser(address, many=True)
            return Response({"address": serializer.data})
        else:
            return render(request, "cart/cart-empty.html")



class EditAddress(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/checkout.html"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        address = Address.objects.filter(user=user)
        serializer = AdressSerialiser(address, many=True)
        return Response({"address": serializer.data})

    def post(self, request, *args, **kwargs):
        address_id = request.data.get("address_id")
        data = {
            "first_name_recivier": request.data.get("first_name_recivier"),
            "last_name_recivier": request.data.get("last_name_recivier"),
            "phone_number_reciver": request.data.get("phone_number_reciver"),
            "apartment_address": request.data.get("apartment_address"),
            "province": request.data.get("province")
        }
        try:
            address = Address.objects.get(id=address_id)
            serializer = AdressSerialiser(address, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return redirect('checkout', slug=request.user.slug)
            else:
                return Response(serializer.errors, status=400)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=404)




# class CreateAddress(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "cart/checkout.html"
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         address = Address.objects.filter(user=user)
#         serializer = AdressSerialiser(address, many=True)
#         return Response({"address": serializer.data})
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         data = {
#             "user": user.id,
#             "first_name_recivier": request.data.get("first_name_recivier"),
#             "last_name_recivier": request.data.get("last_name_recivier"),
#             "phone_number_reciver": request.data.get("phone_number_reciver"),
#             "apartment_address": request.data.get("apartment_address"),
#             "province": request.data.get("province")
#         }
#         serializer = AdressSerialiser(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect('checkout', slug=request.user.slug)
#         else:
#             return Response(serializer.errors, status=400)





class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/order-end.html"

    def get(self, request, *args, **kwargs):
        cart_data = request.session.get("cart_data_obj", {})
        user = request.user
        order = Order.objects.create(user=user)
        for product_id, item_info in cart_data.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity = item_info.get("qty", 1)
            order_item = OrderItem.objects.create(
                order=order,
                item=product,
                quantity=quantity,
            )
        del request.session["cart_data_obj"]
        return Response(
            {
                "id":order.id
            }
        )



class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        order.status = True
        order.save()
        return render(request, "cart/shop_end.html")