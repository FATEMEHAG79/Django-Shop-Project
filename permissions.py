from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from apps.user.models import User, Address
from apps.order.models import Order, OrderItem, Coupon
from apps.shop.models import Product, Comment, Category


manager_group, created = Group.objects.get_or_create(name="product-manager")
operator_group, created = Group.objects.get_or_create(name="operator")
observer_group, created = Group.objects.get_or_create(name="controller")


product_content_type = ContentType.objects.get_for_model(Product)
category_content_type = ContentType.objects.get_for_model(Category)
order_content_type = ContentType.objects.get_for_model(Order)
order_item_content_type = ContentType.objects.get_for_model(OrderItem)
coupon_content_type = ContentType.objects.get_for_model(Coupon)
user_content_type = ContentType.objects.get_for_model(User)
address_content_type = ContentType.objects.get_for_model(Address)
comment_content_type = ContentType.objects.get_for_model(Comment)


manage_product_permissions = Permission.objects.filter(
    content_type=product_content_type
)
manage_comment_permissions = Permission.objects.filter(
    content_type=comment_content_type
)
adress_permissions = Permission.objects.filter(content_type=address_content_type)
manage_category_permissions = Permission.objects.filter(
    content_type=category_content_type
)
manage_copon_permissions = Permission.objects.filter(content_type=coupon_content_type)
view_user_permissions = Permission.objects.filter(content_type=user_content_type)
view_order_permissions = Permission.objects.filter(content_type=order_content_type)
view_orderitem_permissions = Permission.objects.filter(
    content_type=order_item_content_type
)
view_all_permissions = Permission.objects.all()


manager_group.permissions.add(*manage_product_permissions)
manager_group.permissions.add(*manage_category_permissions)
manager_group.permissions.add(*manage_comment_permissions)
manager_group.permissions.add(*manage_copon_permissions)
operator_group.permissions.add(*view_user_permissions)
operator_group.permissions.add(*view_order_permissions)
operator_group.permissions.add(*view_orderitem_permissions)
operator_group.permissions.add(*adress_permissions)
observer_group.permissions.add(*view_all_permissions)
