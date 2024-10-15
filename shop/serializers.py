from rest_framework import serializers
from .models import Product, Category, Rating, DiscountCode, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["product", "score"]


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()  # اضافه کردن این خط

    class Meta:
        model = CartItem
        fields = ["product", "quantity", "total_price"]  # "get_total_price" را حذف کنید

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity  # محاسبه قیمت کل


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    discount_code = DiscountCodeSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "discount_code", "total_price", "created_at"]

    def get_total_price(self, obj):
        total = sum(item.product.price * item.quantity for item in obj.items.all())
        if obj.discount_code and not obj.discount_code.is_used:
            total *= 1 - (obj.discount_code.percentage / 100)
        return total
