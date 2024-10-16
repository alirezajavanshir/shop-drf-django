from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, OtpCode
from rest_framework.views import APIView
from extensions.utils import send_otp
from .serializers import (
    PhoneNumberSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from random import randint


class SendOTPApiView(APIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone_number")
            otp = OtpCode.objects.filter(phone_number=phone).last()
            if not otp:
                otp = randint(1000, 9999)
                OtpCode.objects.get_or_create(phone_number=phone, code=otp)
            send_otp(otp, phone)
            return Response({"info": "کد OTP ارسال شد."}, status=status.HTTP_200_OK)


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp = serializer.validated_data.get("otp")
            phone_number = serializer.validated_data.get("phone_number")
            obj = get_object_or_404(OtpCode, phone_number=phone_number, code=otp)
            obj.delete()
            return Response({"info": "کاربر ایجاد شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            phone_number = serializer.validated_data.get("phone_number")
            password = serializer.validated_data.get("password")

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "خروج موفقیت‌آمیز بود."}, status=status.HTTP_200_OK)
