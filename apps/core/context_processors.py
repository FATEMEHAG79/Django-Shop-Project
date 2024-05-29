from apps.shop.models import Category, Brand, Product


def myquery(request):
    if "cart_data_obj" in request.session:
        totalcartitems = sum(
            item["qty"] for item in request.session["cart_data_obj"].values()
        )
    else:
        totalcartitems = 0
    cart_total_amount = 0
    cart_data = request.session["cart_data_obj"]
    for p_id, item in cart_data.items():
        item["totla_price"] = int(item["qty"]) * float(item["price"])
        product = Product.objects.get(id=p_id)
        item["slug_category"] = product.category.slug
        item["slug"] = product.slug
        cart_total_amount += int(item["qty"]) * float(item["price"])
    cart_data = request.session["cart_data_obj"]
    context = {
        "category": Category.objects.filter(parent=None),
        "totalcartitems": totalcartitems,
        "cart_data": cart_data,
        "brands" : Brand.objects.all()
    }
    return context