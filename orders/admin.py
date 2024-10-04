from django.contrib import admin
from .models import Order, DiscountCode


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "customer",
        "quantity",
        "address",
        "phone",
        "date",
        "status",
    )
    list_filter = ("status", "date")
    search_fields = ("product__name", "customer__username", "address")


admin.site.register(Order, OrderAdmin)
admin.site.register(DiscountCode)
