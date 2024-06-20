from rest_framework import serializers
from apps.shop.models import Media, Product
from apps.order.models import Coupon


# AddToCart
class CartProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    qty = serializers.IntegerField()
    price = serializers.FloatField()


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["file"]


class CartItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    qty = serializers.IntegerField()
    price = serializers.FloatField()
    total_price = serializers.FloatField()
    slug_category = serializers.CharField()
    slug = serializers.CharField()
    media = MediaSerializer(many=True)


class CartProcessor:
    def __init__(self, cart_data, coupon):
        self.cart_data = cart_data
        self.coupon = coupon

    def process_cart(self):
        serialized_data = {}
        cart_total_amount = 0
        total_amount = 0
        for p_id, item in self.cart_data.items():
            product = Product.objects.get(id=p_id)
            media_files = Media.objects.filter(product=product)

            serialized_item = {
                "name": product.name,
                "qty": item["qty"],
                "price": float(item["price"]),
                "total_price": int(item["qty"]) * float(item["price"]),
                "slug_category": product.category.slug,
                "slug": product.slug,
                "media": media_files,
            }

            serializer = CartItemSerializer(serialized_item)
            serialized_data[p_id] = serializer.data
            cart_total_amount += int(item["qty"]) * float(item["price"])
            total_amount += float(product.price) * int(item["qty"])

        if self.coupon:
            code = Coupon.objects.get(code=self.coupon["code"])
            total_discount_amount = float(
                total_amount - cart_total_amount + code.amount,
            )
            cart_total_amount = cart_total_amount - code.amount
        else:
            total_discount_amount = total_amount - cart_total_amount

        return serialized_data, cart_total_amount, total_amount, total_discount_amount


class CouponCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["code", "amount"]
