from rest_framework import permissions, viewsets
from .models import Category, Product, Rating, Cart, CartItem, Discount
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RatingSerializer,
    CartSerializer,
    CartItemSerializer,
    DiscountSerializer,
)
from django.core.exceptions import ValidationError


class IsSuperUser(permissions.BasePermission):
    """
    مجوزی برای اینکه فقط کاربران سوپر یوزر اجازه داشته باشند
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsSuperUser()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsSuperUser()]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # کاربران باید لاگین کنند

    def perform_create(self, serializer):
        user = self.request.user
        if not user.address or not user.postal_code:
            raise ValidationError(
                "لطفاً ابتدا اطلاعات آدرس و کد پستی خود را تکمیل کنید."
            )
        serializer.save(user=user)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]  # کاربران باید لاگین کنند


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]  # کاربران باید لاگین کنند

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
