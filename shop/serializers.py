from rest_framework import serializers
from .models import Menu, MenuItem, Order, Customer
from django.contrib.auth.models import User


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "slug"]


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "menu", "name", "description", "price", "available"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "zipcode",
            "city",
            "country",
        ]


class OrderSerializer(serializers.ModelSerializer):
    product = MenuItemSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
