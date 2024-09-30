from django.contrib import admin
from .models import Menu, MenuItem, Customer, Order


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # تعداد آیتم‌های خالی جدید برای اضافه کردن


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MenuItemInline]


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "menu", "price", "available")
    list_filter = ("available", "menu")
    search_fields = ("name",)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "city")
    search_fields = ("first_name", "last_name", "email")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "quantity", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("customer__first_name", "customer__last_name", "product__name")


# ثبت مدل‌ها در ادمین
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
