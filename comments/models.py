from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(models.Model):
    content = models.TextField(verbose_name="متن کامنت")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
