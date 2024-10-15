from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category_list", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:menu_item_list", kwargs={"menu_item_slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user.username} امتیاز {self.product.name} را با {self.score} داد"


class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class CartItem(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey("Cart", related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    discount_code = models.OneToOneField(
        DiscountCode, null=True, blank=True, on_delete=models.SET_NULL
    )
