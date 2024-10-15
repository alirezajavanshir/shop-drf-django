from django.urls import path
from .views import (
    MenuItemListView,
    MenuItemDetailView,
    CategoryListView,
    CategoryDetailView,
    RatingCreateView,
    ApplyDiscountCodeView,
    CartListCreateView,
    CartItemUpdateDeleteView,
    CheckoutView,
    PaymentView,
)

urlpatterns = [
    path("menu-items/", MenuItemListView.as_view(), name="menuitem-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("rate/", RatingCreateView.as_view(), name="rate_product"),
    path("product/<slug:slug>/", MenuItemDetailView.as_view(), name="menu_item_detail"),
    path("apply-discount/", ApplyDiscountCodeView.as_view(), name="apply-discount"),
    path("cart/", CartListCreateView.as_view(), name="cart-list-create"),
    path(
        "cart/items/<int:pk>/",
        CartItemUpdateDeleteView.as_view(),
        name="cart-item-update-delete",
    ),
    path(
        "cart/apply-discount/", ApplyDiscountCodeView.as_view(), name="apply-discount"
    ),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/", PaymentView.as_view(), name="payment"),
]
