from django.urls import path
from .views import SendOTPView, OTPLoginView, AddressUpdateView

urlpatterns = [
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),
    path("login/", OTPLoginView.as_view(), name="login_with_otp"),
    path("update-address/", AddressUpdateView.as_view(), name="update_address"),
]
