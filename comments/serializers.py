from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "menu_item", "user", "content", "created_at"]
        read_only_fields = ["user", "created_at"]
