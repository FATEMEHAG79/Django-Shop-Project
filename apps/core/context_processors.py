from apps.shop.models import Category, Brand


def myquery(request):
    if "cart_data_obj" in request.session:
        totalcartitems = sum(
            item["qty"] for item in request.session["cart_data_obj"].values()
        )
    else:
        totalcartitems = 0
    context = {
        "category": Category.objects.filter(parent=None),
        "totalcartitems": totalcartitems,
        "brands" : Brand.objects.all()
    }
    return context