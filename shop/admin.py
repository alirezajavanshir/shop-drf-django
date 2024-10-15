from django.contrib import admin
from .models import Product, Category, Rating


@admin.register(Product)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Rating)
