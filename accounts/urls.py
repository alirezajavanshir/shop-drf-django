from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileUpdateView,
    SendOtpView,
    VerifyOtpView,
    CompleteRegistrationView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/update/", UserProfileUpdateView.as_view(), name="profile_update"),
    path("send-otp/", SendOtpView.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify_otp"),
    path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete_registration",
    ),
]
