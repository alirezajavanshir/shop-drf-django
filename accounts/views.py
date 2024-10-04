from django.core.cache import cache
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileUpdateSerializer
import random


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SendOtpView(views.APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            otp_code = str(random.randint(1000, 9999))
            cache.set(phone_number, otp_code, timeout=300)
            print(phone_number, "----", otp_code)
            return Response(
                {"message": "کد OTP با موفقیت ارسال شد."}, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "کاربر وجود ندارد."}, status=status.HTTP_404_NOT_FOUND
            )


class VerifyOtpView(views.APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = request.data.get("otp_code")

        cached_otp = cache.get(phone_number)

        if cached_otp is None:
            return Response(
                {"error": "کد OTP منقضی شده یا ارسال نشده است."},
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
        phone_number = request.data.get("phone_number")
        address = request.data.get("address")
        postal_code = request.data.get("postal_code")

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            user.address = address
            user.postal_code = postal_code
            user.otp_verified = True  # یا هر فیلدی که نیاز دارید
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
