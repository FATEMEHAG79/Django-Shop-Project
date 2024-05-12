from rest_framework.response import Response
from rest_framework.views import APIView


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
                cart_data[str(request.GET["id"])]["qty"] = int(request.GET["qty"])
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
                "totalcartitems": len(request.session["cart_data_obj"]),
            }
        )
