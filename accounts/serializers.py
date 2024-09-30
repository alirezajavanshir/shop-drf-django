from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp_code = serializers.CharField(max_length=6, required=False)


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["address", "postal_code"]
