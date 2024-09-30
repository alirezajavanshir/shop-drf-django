from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer", "quantity", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("product__name", "customer__phone_number")
