from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.order.models import Order, OrderItem, Product, Coupon
from apps.user.models import Address
from apps.order.serializers import CartProductSerializer, CartProcessor
from rest_framework.permissions import IsAuthenticated


class AddToCartAPI(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CartProductSerializer(data=request.GET)

        if serializer.is_valid():
            product_id = serializer.validated_data["id"]
            cart_product = {
                product_id: {
                    "name": serializer.validated_data["name"],
                    "qty": serializer.validated_data["qty"],
                    "price": serializer.validated_data["price"],
                }
            }

            if "cart_data_obj" in request.session:
                cart_data = request.session["cart_data_obj"]
                if product_id in cart_data:
                    cart_data[product_id]["qty"] += serializer.validated_data["qty"]
                else:
                    cart_data.update(cart_product)
                request.session["cart_data_obj"] = cart_data
            else:
                request.session["cart_data_obj"] = cart_product

            return Response(
                {
                    "data": request.session["cart_data_obj"],
                    "totalcartitems": sum(
                        item["qty"]
                        for item in request.session["cart_data_obj"].values()
                    ),
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/cart.html"

    def get(self, request):
        cart_data = request.session.get("cart_data_obj", {})
        coupon = request.session.get("coupon", {})
        if cart_data:
            processor = CartProcessor(cart_data, coupon)
            serialized_data, cart_total_amount, total_amount, total_discount_amount = (
                processor.process_cart()
            )
            total_cart_items = sum(item["qty"] for item in cart_data.values())

            return Response(
                {
                    "cart_data": serialized_data,
                    "total_cart_items": total_cart_items,
                    "cart_total_amount": cart_total_amount,
                    "total_discount_amount": total_amount - cart_total_amount,
                    "total_amount": total_amount,
                },
                template_name=self.template_name,
            )
        else:
            return render(request, template_name="cart/cart-empty.html")


class DeleteItemCart(APIView):
    def get(self, request):
        item_id = str(request.GET["id_item"])
        if "cart_data_obj" in request.session:
            if item_id in request.session["cart_data_obj"]:
                cart_data = request.session["cart_data_obj"]
                del request.session["cart_data_obj"][item_id]
                request.session["cart_data_obj"] = cart_data

        cart_data = request.session.get("cart_data_obj", {})
        coupon = request.session.get("coupon", {})
        processor = CartProcessor(cart_data, coupon)
        serialized_data, cart_total_amount, total_amount, total_discount_amount = (
            processor.process_cart()
        )
        total_cart_items = sum(item["qty"] for item in cart_data.values())
        context = render_to_string(
            "cart/cart_list.html",
            {
                "cart_data": serialized_data,
                "total_cart_items": total_cart_items,
                "cart_total_amount": cart_total_amount,
                "total_discount_amount": total_discount_amount,
            },
        )
        return Response(
            {
                "data": context,
            }
        )


class UpdateItemCart(APIView):
    def get(self, request):
        item_id = str(request.GET["id"])
        item_qty = int(request.GET["qty"])
        if "cart_data_obj" in request.session:
            if item_id in request.session["cart_data_obj"]:
                cart_data = request.session["cart_data_obj"]
                cart_data[item_id]["qty"] = item_qty
                request.session["cart_data_obj"] = cart_data

        cart_data = request.session.get("cart_data_obj", {})
        coupon = request.session.get("coupon", {})
        if cart_data:
            processor = CartProcessor(cart_data, coupon)
            serialized_data, cart_total_amount, total_amount, total_discount_amount = (
                processor.process_cart()
            )
            total_cart_items = sum(item["qty"] for item in cart_data.values())
            context = render_to_string(
                "cart/cart_list.html",
                {
                    "cart_data": serialized_data,
                    "total_cart_items": total_cart_items,
                    "cart_total_amount": cart_total_amount,
                    "total_discount_amount": total_discount_amount,
                },
            )
            return Response(
                {
                    "data": context,
                }
            )
        else:
            return render(request, template_name="cart/cart-empty.html")


class Checkout(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/checkout.html"

    def get(self, request):
        cart_data = request.session.get("cart_data_obj", {})
        coupon = request.session.get("coupon", {})
        if cart_data:
            processor = CartProcessor(cart_data, coupon)
            serialized_data, cart_total_amount, total_amount, total_discount_amount = (
                processor.process_cart()
            )
            total_cart_items = sum(item["qty"] for item in cart_data.values())
            address = Address.objects.filter(user=request.user)
            return Response(
                {
                    "cart_data": serialized_data,
                    "total_cart_items": total_cart_items,
                    "cart_total_amount": cart_total_amount,
                    "total_discount_amount": total_discount_amount,
                    "total_amount": total_amount,
                    "address": address,
                },
                template_name=self.template_name,
            )
        else:
            return render(request, template_name="cart/cart-empty.html")


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/order-end.html"

    def get(self, request, *args, **kwargs):
        cart_data = request.session.get("cart_data_obj", {})
        user = request.user
        selected_address_id = request.GET.get("selectedAddress")
        if not selected_address_id:
            return Response({"error": "Address not selected"}, status=400)

        address = get_object_or_404(Address, id=selected_address_id)

        order = Order.objects.create(user=user, address=address)
        for product_id, item_info in cart_data.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity = item_info.get("qty", 1)
            OrderItem.objects.create(order=order, item=product, quantity=quantity)

        del request.session["cart_data_obj"]
        return Response({"id": order.id})

    def post(self, request, *args, **kwargs):
        cart_data = request.session.get("cart_data_obj", {})
        user = request.user
        selected_address_id = request.POST.get("selectedAddress")
        if not selected_address_id:
            return Response({"error": "Address not selected"}, status=400)

        address = get_object_or_404(Address, id=selected_address_id)
        coupon = request.session.get("code")
        order = Order.objects.create(user=user, address=address, coupon=coupon)
        for product_id, item_info in cart_data.items():
            product = get_object_or_404(Product, pk=product_id)
            quantity = item_info.get("qty", 1)
            OrderItem.objects.create(order=order, item=product, quantity=quantity)

        del request.session["cart_data_obj"]
        return Response({"id": order.id})


class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        order.status = True
        order.save()
        return render(request, "cart/shop_end.html")


class ApplyCouponView(APIView):
    def post(self, request):
        code = self.request.POST.get("code")
        coupon = Coupon.objects.get(code=code)
        if not coupon:
            return HttpResponse("Invalid code.")
        else:
            request.session["coupon"] = {"code": code}
            return redirect(
                "cart",
            )
