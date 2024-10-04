from rest_framework import generics, permissions, viewsets
from .models import Order, DiscountCode
from .serializers import OrderSerializer, DiscountCodeSerializer
from rest_framework.response import Response


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.address:
            return Response(
                {"error": "لطفاً اطلاعات پروفایل خود را تکمیل کنید."}, status=400
            )

        serializer.save(customer=user)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
