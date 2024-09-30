from django.urls import path
from .views import (
    MenuItemListView,
    MenuItemDetailView,
    CategoryListView,
    CategoryDetailView,
)

urlpatterns = [
    path("menu-items/", MenuItemListView.as_view(), name="menuitem-list"),
    path(
        "menu-items/<slug:slug>/", MenuItemDetailView.as_view(), name="menuitem-detail"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]
