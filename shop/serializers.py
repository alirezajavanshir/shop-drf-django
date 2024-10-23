from rest_framework import serializers
from .models import Category, Product, Rating, Discount  # Cart, CartItem,


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


"""
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items")
        instance.save()
        for item_data in items_data:
            item_id = item_data.get("id", None)
            if item_id:
                item = CartItem.objects.get(id=item_id, cart=instance)
                item.quantity = item_data.get("quantity", item.quantity)
                item.save()
            else:
                CartItem.objects.create(cart=instance, **item_data)
        return instance

"""


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"

    def validate(self, attrs):
        user = attrs.get("user")
        discount_code = attrs.get("discountCode")

        # بررسی اینکه آیا کاربر قبلاً از این کد تخفیف استفاده کرده یا نه
        if Discount.objects.filter(
            user=user, discountCode=discount_code, used=True
        ).exists():
            raise serializers.ValidationError("این کد تخفیف قبلاً استفاده شده است.")
        return attrs
