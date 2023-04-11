from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Order, OrderItem, Product


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "id", "username"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ["url", "name", "price", "stock", "isbn_no"]


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["url", "id", "order", "product", "price", "quantity"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.HyperlinkedRelatedField(many=True, view_name="orderitem-detail", read_only=True)

    class Meta:
        model = Order
        fields = [
            "url",
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "city",
            "created",
            "updated",
            "paid",
            "items",
        ]
