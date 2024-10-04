from django.urls import path
from .views import (
    MenuItemListView,
    MenuItemDetailView,
    CategoryListView,
    CategoryDetailView,
    RatingCreateView,
)

urlpatterns = [
    path("menu-items/", MenuItemListView.as_view(), name="menuitem-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("rate/", RatingCreateView.as_view(), name="rate_product"),
    path("product/<slug:slug>/", MenuItemDetailView.as_view(), name="menu_item_detail"),
]
