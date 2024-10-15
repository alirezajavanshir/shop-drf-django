from rest_framework import serializers
from .models import CustomUser
from django.core.cache import cache
import random


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "address", "postal_code"]

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return value

    def create(self, validated_data):
        # تولید کد OTP و ذخیره آن در کش
        otp_code = str(random.randint(1000, 9999))
        cache.set(validated_data["phone_number"], otp_code, timeout=300)

        user = CustomUser(**validated_data)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "address", "postal_code"]
        read_only_fields = ["phone_number"]

    def validate(self, data):
        # بررسی تکمیل بودن اطلاعات
        if not all(
            [
                data.get("first_name"),
                data.get("last_name"),
                data.get("address"),
                data.get("postal_code"),
            ]
        ):
            raise serializers.ValidationError("تمامی فیلدها باید تکمیل شوند.")
        return data


class CompleteRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    address = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        user = CustomUser.objects.filter(phone_number=data["phone_number"]).first()
        if not user:
            raise serializers.ValidationError("کاربری با این شماره تلفن پیدا نشد.")

        # بررسی کد OTP از کش
        cached_otp = cache.get(data["phone_number"])
        if cached_otp is None or cached_otp != data["otp_code"]:
            raise serializers.ValidationError("کد OTP نادرست است یا منقضی شده است.")

        return data


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        if not CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("کاربری با این شماره تلفن پیدا نشد.")

        return attrs
