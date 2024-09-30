from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Menu, MenuItem, Order, Customer
from .serializers import (
    MenuSerializer,
    MenuItemSerializer,
    OrderSerializer,
    CustomerSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


# سبد خرید
class CartAPIView(APIView):
    def get_cart(self, request):

        return request.session.get("cart", {})

    def update_cart(self, request, item_id, action):

        cart = self.get_cart(request)

        if action == "add":
            item = MenuItem.objects.get(id=item_id)

            if str(item_id) in cart:
                cart[str(item_id)]["quantity"] += 1
            else:
                cart[str(item_id)] = {
                    "name": item.name,
                    "price": str(item.price),
                    "quantity": 1,
                }
        elif action == "remove" and str(item_id) in cart:
            del cart[str(item_id)]

        request.session["cart"] = cart
        request.session.modified = True

    def post(self, request, item_id):
        self.update_cart(request, item_id, "add")
        return Response(
            {"message": "آیتم به سبد خرید افزوده شد."}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, item_id):
        self.update_cart(request, item_id, "remove")
        return Response(
            {"message": "آیتم از سبد خرید حذف شد."}, status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request):
        cart = self.get_cart(request)
        return Response(cart, status=status.HTTP_200_OK)


# پردازش سفارش
class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.session.get("cart", {})
        if not cart:
            return Response(
                {"error": "سبد خرید خالی است."}, status=status.HTTP_400_BAD_REQUEST
            )

        customer = Customer.objects.get(id=request.data.get("customer_id"))

        for item_id, item_details in cart.items():
            Order.objects.create(
                product=MenuItem.objects.get(id=item_id),
                customer=customer,
                quantity=item_details["quantity"],
                address=request.data.get("address", ""),
                phone=request.data.get("phone", ""),
            )

        del request.session["cart"]
        return Response(
            {"message": "سفارش با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED
        )


# منو
class MenuListView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


# آیتم‌های منو
class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# مشتری
class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


# ثبت‌نام کاربر
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not email or not password:
            return Response(
                {"error": "همه فیلد ها ضروری است"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return Response(
            {"message": "ثبت نام با موفقیت انجام شد"}, status=status.HTTP_201_CREATED
        )
