"""
تنظیمات Django برای پروژه فروشگاه.

توسط 'django-admin startproject' با استفاده از Django 5.1 تولید شده است.

برای اطلاعات بیشتر در مورد این فایل، به
https://docs.djangoproject.com/en/5.1/topics/settings/ مراجعه کنید.

برای لیست کامل تنظیمات و مقادیر آن‌ها، به
https://docs.djangoproject.com/en/5.1/ref/settings/ مراجعه کنید.
"""

from pathlib import Path
import os

# ساخت مسیرها درون پروژه مانند این: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# تنظیمات سریع برای توسعه - نامناسب برای تولید
# به چک‌لیست استقرار Django برای جزئیات بیشتر مراجعه کنید

# هشدار امنیتی: کلید مخفی را در تولید مخفی نگه دارید!
SECRET_KEY = "django-insecure-pp-@^)$==-io$w9g279n9m(^qx5#*6a@d(+16r5(p0l)6_pp-$"

# هشدار امنیتی: با فعال بودن حالت اشکال‌زدایی در تولید اجرا نکنید!
DEBUG = True

ALLOWED_HOSTS = []


# تعریف برنامه‌ها

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop.apps.ShopConfig",
    "unidecode",
    "rest_framework",
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # my change
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# پایگاه داده
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# اعتبارسنجی رمز عبور
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# بین‌المللی‌سازی
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "fa-ir"  # کد زبان فارسی
TIME_ZONE = "Asia/Tehran"  # منطقه زمانی ایران

USE_I18N = True

USE_TZ = True


# فایل‌های استاتیک (CSS، JavaScript، تصاویر)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = []


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# نوع فیلد کلید اصلی پیش‌فرض
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
