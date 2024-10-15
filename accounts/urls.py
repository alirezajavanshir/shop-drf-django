from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    SendOtpView,
    VerifyOtpView,
    CompleteRegistrationView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("send-otp/", SendOtpView.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify_otp"),
    path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete_registration",
    ),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
