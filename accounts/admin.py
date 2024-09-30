from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "is_active", "is_staff")
    search_fields = ("phone_number",)
