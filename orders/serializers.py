from rest_framework import serializers
from .models import Order
from shop.serializers import MenuItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = MenuItemSerializer(read_only=True)
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "customer",
            "quantity",
            "address",
            "phone",
            "date",
            "status",
        ]
