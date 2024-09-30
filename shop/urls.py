from django.urls import path
from django.contrib import admin
from .views import (
    MenuListView,
    MenuDetailView,
    MenuItemListView,
    MenuItemDetailView,
    CustomerListView,
    CustomerDetailView,
    OrderAPIView,
    RegisterUserView,
    CartAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLهای منو
    path("menus/", MenuListView.as_view(), name="menu-list"),
    path("menus/<slug:slug>/", MenuDetailView.as_view(), name="menu-detail"),
    # URLهای آیتم‌های منو
    path("menu-items/", MenuItemListView.as_view(), name="menuitem-list"),
    path("menu-items/<int:pk>/", MenuItemDetailView.as_view(), name="menuitem-detail"),
    # URLهای مشتری
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    # URLهای سفارش
    path("orders/", OrderAPIView.as_view(), name="process-order"),
    # ثبت‌نام کاربر
    path("register/", RegisterUserView.as_view(), name="register"),
    # URLهای سبد خرید
    path("cart/", CartAPIView.as_view(), name="cart"),  # برای دریافت و مدیریت سبد خرید
    path(
        "cart/<int:item_id>/", CartAPIView.as_view(), name="cart-item"
    ),  # برای افزودن یا حذف آیتم
]
