from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "user", "content", "created_at")
    list_filter = ("menu_item", "user")
    search_fields = ("content",)


admin.site.register(Comment, CommentAdmin)
