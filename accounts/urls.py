from django.urls import path
from .views import OTPLoginView, AddressUpdateView

urlpatterns = [
    path("login/", OTPLoginView.as_view(), name="login_with_otp"),
    path("update-address/", AddressUpdateView.as_view(), name="update_address"),
]
