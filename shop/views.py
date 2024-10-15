from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, DiscountCode, Cart, CartItem
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    RatingSerializer,
    DiscountCodeSerializer,
    CartItemSerializer,
    CartSerializer,
)


class MenuItemListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuItemDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_products"] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)
        return context


class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()


class ApplyDiscountCodeView(generics.GenericAPIView):
    serializer_class = DiscountCodeSerializer

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        code = request.data.get("code")

        try:
            discount_code = DiscountCode.objects.get(
                code=code, user=request.user, is_active=True, used=False
            )
        except DiscountCode.DoesNotExist:
            return Response(
                {"error": "کد تخفیف نامعتبر است یا قبلاً استفاده شده."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart.discount_code = discount_code
        cart.save()

        return Response(
            {"message": "کد تخفیف با موفقیت اعمال شد."}, status=status.HTTP_200_OK
        )


class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_profile_complete():
            return Response(
                {"detail": "لطفاً ابتدا اطلاعات پروفایل خود را تکمیل کنید."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            # منطق مربوط به نمایش اطلاعات تسویه‌حساب یا ادامه فرآیند
            return Response(
                {"detail": "می‌توانید به مرحله پرداخت بروید."}, status=status.HTTP_200_OK
            )


class PaymentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # بررسی مجدد کامل بودن پروفایل
        if not user.is_profile_complete():
            return Response(
                {"detail": "لطفاً ابتدا اطلاعات پروفایل خود را تکمیل کنید."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # منطق پرداخت
        # ...
        return Response(
            {"detail": "پرداخت با موفقیت انجام شد."}, status=status.HTTP_200_OK
        )
