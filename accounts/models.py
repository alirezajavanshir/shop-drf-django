import random
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره تلفن باید مشخص شود")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.generate_otp()  # تولید کد OTP هنگام ایجاد کاربر
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("کاربر سوپر باید is_staff=True داشته باشد.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("کاربر سوپر باید is_superuser=True داشته باشد.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name="شماره تلفن"
    )
    is_staff = models.BooleanField(default=False, verbose_name="کاربر کارمندی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_superuser = models.BooleanField(default=False, verbose_name="سوپرکاربر")
    address = models.TextField(blank=True, verbose_name="آدرس")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="کد پستی")
    otp_code = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="کد OTP"
    )
    first_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="نام خانوادگی"
    )
    otp_verified = models.BooleanField(default=False, verbose_name="تأیید شده OTP")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def is_profile_complete(self):
        return all(
            [
                self.phone_number,
                self.address,
                self.postal_code,
                self.first_name,
                self.last_name,
            ]
        )

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.save()

    def verify_otp(self, input_code):
        if self.otp_code == input_code:
            self.otp_verified = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.phone_number
