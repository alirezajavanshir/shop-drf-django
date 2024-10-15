from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    PhoneNumberSerializer,
    CompleteRegistrationSerializer,
    LoginSerializer,
)
import random


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        # تولید کد OTP و ارسال آن
        otp_code = str(random.randint(1000, 9999))
        cache.set(phone_number, otp_code, timeout=300)
        print(phone_number, "----", otp_code)  # برای دیباگ

        # ثبت‌نام کاربر و ارسال کد OTP
        self.perform_create(serializer)
        return Response(
            {"message": "کد OTP با موفقیت ارسال شد."}, status=status.HTTP_201_CREATED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SendOtpView(views.APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if not user:
            return Response(
                {"error": "کاربر با این شماره تلفن وجود ندارد."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # بررسی اینکه آیا کاربر OTP قبلی دارد
        existing_otp = cache.get(phone_number)
        if existing_otp:
            return Response(
                {"message": "کد OTP قبلی هنوز معتبر است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_code = str(random.randint(1000, 9999))
        cache.set(phone_number, otp_code, timeout=300)
        print(phone_number, "----", otp_code)  # برای دیباگ
        return Response(
            {"message": "کد OTP با موفقیت ارسال شد."}, status=status.HTTP_200_OK
        )


class VerifyOtpView(views.APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        otp_code = request.data.get("otp_code")

        cached_otp = cache.get(phone_number)

        if cached_otp is None:
            return Response(
                {"error": "کد OTP شما منقضی شده است. لطفاً دوباره درخواست دهید."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cached_otp == otp_code:
            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
            if created:
                return Response(
                    {"message": "کد OTP تأیید شد. لطفاً ثبت‌نام خود را کامل کنید."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "کاربر قبلاً وجود دارد."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "کد OTP نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST
            )


class CompleteRegistrationView(views.APIView):
    def post(self, request):
        serializer = CompleteRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        address = serializer.validated_data["address"]
        postal_code = serializer.validated_data["postal_code"]

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            user.address = address
            user.postal_code = postal_code
            user.otp_verified = True
            user.save()
            cache.delete(phone_number)  # حذف OTP از کش
            return Response(
                {"message": "ثبت‌نام با موفقیت کامل شد."},
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "کاربر وجود ندارد."}, status=status.HTTP_404_NOT_FOUND
            )


class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        # احراز هویت کاربر
        user = authenticate(request, username=phone_number, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"message": "ورود موفقیت‌آمیز بود."}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": "شماره تلفن یا رمز عبور نادرست است."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "خروج موفقیت‌آمیز بود."}, status=status.HTTP_200_OK)
