from django.db import models
import datetime
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام منو")
    slug = models.SlugField(
        max_length=100, unique=True, allow_unicode=True, verbose_name="آدرس منو"
    )

    class Meta:
        verbose_name = "منو"
        verbose_name_plural = "منوها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu_detail", kwargs={"slug": self.slug})


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu, related_name="items", on_delete=models.CASCADE, verbose_name="منو"
    )
    name = models.CharField(max_length=100, verbose_name="نام آیتم منو")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    available = models.BooleanField(default=True, verbose_name="موجود")
    image = models.ImageField(
        upload_to="menu_items/", blank=True, null=True, verbose_name="عکس"
    )

    class Meta:
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم‌های منو"

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")
    address = models.CharField(max_length=100, verbose_name="آدرس")
    zipcode = models.CharField(max_length=10, verbose_name="کد پستی")
    city = models.CharField(max_length=20, verbose_name="شهر")
    country = models.CharField(max_length=20, verbose_name="کشور")
    password = models.CharField(max_length=20, verbose_name="رمز عبور")

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    product = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, verbose_name="محصول"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="مشتری"
    )
    quantity = models.IntegerField(default=1, verbose_name="تعداد")
    address = models.CharField(
        max_length=200, default="", blank=True, verbose_name="آدرس"
    )
    phone = models.CharField(
        max_length=20, default="", blank=True, verbose_name="شماره تلفن"
    )
    date = models.DateField(default=datetime.date.today, verbose_name="تاریخ")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ("-date",)  # ترتیب بر اساس تاریخ
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"سفارش {self.product.name} برای {self.customer.first_name} {self.customer.last_name}"
