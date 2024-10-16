from django.contrib import admin
from .models import Category, Product, Rating, Cart, CartItem, Discount


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")  # نمایش نام و والد در لیست
    search_fields = ("name",)  # جستجو بر اساس نام دسته‌بندی
    list_filter = ("parent",)  # فیلتر بر اساس والد


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")  # نمایش نام، دسته‌بندی و قیمت محصول
    search_fields = ("name", "description")  # جستجو بر اساس نام و توضیحات
    list_filter = ("category",)  # فیلتر بر اساس دسته‌بندی


class RatingAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "score")  # نمایش محصول، کاربر و امتیاز
    search_fields = ("user__username",)  # جستجو بر اساس نام کاربر


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "updated_at",
    )  # نمایش کاربر، زمان ایجاد و زمان به‌روزرسانی
    search_fields = ("user__username",)  # جستجو بر اساس نام کاربر


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")  # نمایش سبد خرید، محصول و مقدار
    search_fields = ("product__name",)  # جستجو بر اساس نام محصول


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "discountCode",
        "valueDecimal",
        "used",
    )  # نمایش کاربر، کد تخفیف، ارزش و استفاده شده
    search_fields = ("discountCode",)  # جستجو بر اساس کد تخفیف


# ثبت مدل‌ها در ادمین
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Discount, DiscountAdmin)
