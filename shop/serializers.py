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
        fields = ["code", "discount_percent", "user", "is_active", "used", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ["product", "quantity", "get_total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    discount_code = DiscountCodeSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "discount_code", "total_price", "created_at"]

    def get_total_price(self, obj):
        return obj.get_total_price()
