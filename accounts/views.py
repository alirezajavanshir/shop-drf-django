from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    OTPVerifySerializer,
    LoginSerializer,
)
import random

User = get_user_model()


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            # تولید کد تصادفی OTP
            otp_code = random.randint(1000, 9999)
            # ذخیره کردن OTP در کش برای 5 دقیقه
            cache.set(phone_number, otp_code, timeout=300)
            # ارسال کد OTP به شماره تلفن
            # اینجا باید کد ارسال OTP توسط SMS قرار بگیرد
            # send_otp(otp_code, phone_number)

            # ذخیره اطلاعات کاربر در سشن برای استفاده بعد از تایید کد
            request.session["user_registration_info"] = serializer.validated_data

            return Response(
                {"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            entered_code = serializer.validated_data["code"]

            # گرفتن کد OTP از کش
            cached_code = cache.get(phone_number)

            if cached_code is None:
                return Response(
                    {"error": "OTP expired or invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if str(cached_code) != entered_code:
                return Response(
                    {"error": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST
                )

            # اگر OTP درست بود، کاربر ثبت‌نام می‌شود
            user_data = request.session.get("user_registration_info")
            if not user_data:
                return Response(
                    {"error": "No registration information found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create_user(
                phone_number=user_data["phone_number"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                password=user_data["password"],
            )

            # کاربر لاگین می‌شود
            login(request, user)

            # پاک کردن اطلاعات سشن و OTP
            del request.session["user_registration_info"]
            cache.delete(phone_number)

            return Response(
                {"message": "User registered and logged in successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid phone number or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
