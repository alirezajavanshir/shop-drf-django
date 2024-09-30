import random
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, login
from .serializers import OTPLoginSerializer, AddressUpdateSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


def generate_otp():
    return str(random.randint(100000, 999999))


def store_otp(phone_number, otp_code):
    cache.set(f"otp_{phone_number}", otp_code, timeout=300)  # 5 minutes


def retrieve_otp(phone_number):
    return cache.get(f"otp_{phone_number}")


def send_otp(phone_number, otp_code):
    print(f"Sending OTP {otp_code} to {phone_number}")


class OTPLoginView(APIView):
    def post(self, request):
        serializer = OTPLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp_code = serializer.validated_data.get("otp_code")

            if otp_code:
                stored_otp = retrieve_otp(phone_number)
                if otp_code == stored_otp:
                    try:
                        user = User.objects.get(phone_number=phone_number)
                        login(request, user)
                        return Response(
                            {"detail": "ورود با موفقیت انجام شد"},
                            status=status.HTTP_200_OK,
                        )
                    except User.DoesNotExist:
                        return Response(
                            {"detail": "کاربر پیدا نشد"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                else:
                    return Response(
                        {"detail": "OTP نامعتبر است"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                otp_code = generate_otp()
                store_otp(phone_number, otp_code)
                send_otp(phone_number, otp_code)
                return Response({"detail": "OTP ارسال شد"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddressUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "آدرس با موفقیت به‌روز شد"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
