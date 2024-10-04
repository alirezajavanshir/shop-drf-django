from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        menu_item_id = self.kwargs["menu_item_id"]
        return Comment.objects.filter(menu_item_id=menu_item_id)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)
