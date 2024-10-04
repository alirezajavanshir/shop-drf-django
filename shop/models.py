from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:menu_item_list", kwargs={"menu_item_slug": self.slug})

    def save(self, *args, **kwargs):
        slug = ""
        for char in self.name:  # تغییر title به name
            if char.isalpha():
                slug += char
            elif char == " ":
                slug += "-"
        self.slug = slug
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category_list", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        slug = ""
        for char in self.name:  # تغییر title به name
            if char.isalpha():
                slug += char
            elif char == " ":
                slug += "-"
        self.slug = slug
        super().save(*args, **kwargs)


class Rating(models.Model):
    product = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user.username} امتیاز {self.product.name} را با {self.score} داد"
