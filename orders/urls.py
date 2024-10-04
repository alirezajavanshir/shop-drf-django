from .views import OrderCreateView, OrderListView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiscountCodeViewSet

router = DefaultRouter()
router.register(r"discount-codes", DiscountCodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("list/", OrderListView.as_view(), name="order_list"),
]
