from apps.shop.models import Category, Brand, Product, Media


def myquery(request):
    if "cart_data_obj" in request.session:
        cart_data = request.session["cart_data_obj"]
        totalcartitems = sum(item["qty"] for item in cart_data.values())
    else:
        cart_data = {}
        totalcartitems = 0

    cart_total_amount = 0

    for p_id, item in cart_data.items():
        item["total_price"] = int(item["qty"]) * float(item["price"])
        product = Product.objects.get(id=p_id)
        item["slug_category"] = product.category.slug
        item["slug"] = product.slug
        media_files = Media.objects.filter(product=product)
        item["media"] = media_files
        cart_total_amount += int(item["qty"]) * float(item["price"])

    context = {
        "category": Category.objects.filter(parent=None),
        "totalcartitems": totalcartitems,
        "cart_data": cart_data,
        "cart_total_amount": cart_total_amount,
        "brands": Brand.objects.all(),
    }
    return context
