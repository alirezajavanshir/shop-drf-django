from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path(
        "menu-items/<int:menu_item_id>/comments/",
        CommentListCreateView.as_view(),
        name="menu-item-comments",
    ),
]
