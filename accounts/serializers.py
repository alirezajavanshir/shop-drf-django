from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "address", "postal_code"]


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
