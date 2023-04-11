from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["url", "id", "order", "product", "price", "quantity", "get_cost"]


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
