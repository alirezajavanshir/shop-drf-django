from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    RatingViewSet,
    # CartViewSet,
    # CartItemViewSet,
    DiscountViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"ratings", RatingViewSet)
# router.register(r"carts", CartViewSet)
# router.register(r"cart-items", CartItemViewSet)
router.register(r"discounts", DiscountViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
