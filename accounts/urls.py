from django.urls import path
from .views import (
    SendOTPApiView,
    RegisterApiView,
    LogoutApiView,
    LoginApiView,
)

urlpatterns = [
    path("register/", SendOTPApiView.as_view(), name="register"),
    path("verify-otp/", RegisterApiView.as_view(), name="verify_otp"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
]
