from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "address",
        "postal_code",
        "is_active",
        "is_staff",
    )
    search_fields = ("phone_number",)
