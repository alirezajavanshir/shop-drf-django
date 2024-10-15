from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product
from django.conf import settings

User = get_user_model()


class Comment(models.Model):
    menu_item = models.ForeignKey(
        Product, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    content = models.TextField(verbose_name="متن کامنت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"کامنت از {self.user} بر روی {self.menu_item}"
