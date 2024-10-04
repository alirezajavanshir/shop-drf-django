from rest_framework import serializers
from .models import Order
from .models import DiscountCode


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ["id", "code", "discount_percentage", "expiration_date", "products"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "product",
            "customer",
            "quantity",
            "address",
            "phone",
            "discount_code",
        ]

    def create(self, validated_data):
        # شما می‌توانید کد تخفیف را اینجا بررسی کنید
        order = Order.objects.create(**validated_data)
        return order
